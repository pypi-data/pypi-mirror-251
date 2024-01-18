import asyncio
import signal
import traceback
from typing import TYPE_CHECKING

import networkx as nx
import ray

from ronds_sdk import logger_config
from ronds_sdk.options.pipeline_options import RayOptions
from ronds_sdk.runners.planners import OrderedPlanner
from ronds_sdk.runners.planners.core_rules import CoreRules
from ronds_sdk.runners.runner import PipelineRunner, PipelineResult
from ronds_sdk.tools import utils
from ronds_sdk.tools.networkx_util import NetworkUtil

if TYPE_CHECKING:
    from ronds_sdk.transforms.ray.base import RayPhyTransform
    from ronds_sdk import Pipeline, logger_config

logger = logger_config.config()


class RayStreamRunner(PipelineRunner):

    def __init__(self, options):
        super().__init__(options)
        self._ray_options = options.view_as(RayOptions)
        self._rules = self._ray_options.runer_planner_rules()
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def _handle_signal(self, signum, frame):
        logger.info("SIGTERM signal received, stopping ray: %s" % signum)
        ray.shutdown()

    @property
    def rules(self):
        if self._rules is None:
            self._rules = [
                CoreRules.RAY_BASIC_PARAM_RULE,
                CoreRules.RAY_PARALLEL_RULE,
                CoreRules.RAY_STREAM_CONVERT_RULE,
                CoreRules.RAY_MERGE_SINGLE_RULE,
                CoreRules.RAY_PLACEMENT_GROUP_RULE,
                CoreRules.RAY_STREAM_PHYSICAL_RULE,
            ]
            if not self._ray_options.is_merge():
                self._rules.remove(CoreRules.RAY_MERGE_SINGLE_RULE)
        return self._rules

    def run_pipeline(self, pipeline, options):
        ray.init()

        p = OrderedPlanner(self.rules).find_best(pipeline)
        if self._ray_options.is_draw_pipeline():
            from ronds_sdk.tools import utils
            utils.draw_graph(p.graph, title='run_pipeline')
        self.bind_stream(p)
        self.startup(p)
        logger.info("Pipeline started!")
        return RayResult(p)

    def bind_stream(self, p):
        visited = set()
        from ronds_sdk.tools.networkx_util import NetworkUtil
        for root_node in NetworkUtil.get_root_nodes(p.graph):  # type: RayPhyTransform
            for node in NetworkUtil.bfs_nodes(root_node, p.graph):  # type: RayPhyTransform
                if node in visited:
                    continue
                visited.add(node)

                self._bind_down(node, p)
                self._bind_up(node, p)
                logger.info("node: %s, keys: %s" % (str(node), node.keys()))

    @staticmethod
    def _bind_down(node: 'RayPhyTransform', p: 'Pipeline'):
        successors = list(p.successors(node))
        if utils.collection_empty(successors):
            return
        for successor in successors:  # type: RayPhyTransform
            node.bind_downstream(successor.consumer_id, successor)

    @staticmethod
    def _bind_up(node: 'RayPhyTransform', p: 'Pipeline'):
        predecessors = list(p.graph.predecessors(node))
        if utils.collection_empty(predecessors):
            return
        for predecessor in predecessors:
            node.bind_upstream(predecessor.consumer_id, predecessor)

    def startup(self, p):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.parallel_startup(p))
        loop.run_until_complete(task)

    async def parallel_startup(self, p, parallel=3):
        try:
            semaphore = asyncio.Semaphore(parallel)
            async with semaphore:
                for nodes in nx.weakly_connected_components(p.graph):
                    if utils.collection_empty(nodes):
                        continue
                    await self._startup(nodes, p)
        except Exception as e:
            logger.error("startup error: %s, \n%s" % (e, traceback.format_exc()))
            ray.shutdown()

    @staticmethod
    async def _startup(nodes, p: 'Pipeline'):
        visited = set()
        for r_node in nodes:  # type: RayPhyTransform
            if p.graph.in_degree(r_node) > 0:
                continue
            for node in NetworkUtil.dfs_postorder_nodes(p.graph, root_node=r_node):  # type: RayPhyTransform
                if node in visited:
                    continue
                visited.add(node)
                await node.deploy()
                await node.startup()
        assert len(visited) == len(nodes)
        # check job startup or not
        for node in visited:
            if not await node.is_startup():
                logger.error("startup failed: %s" % node)
                ray.shutdown()


class RayResult(PipelineResult):

    def __init__(self, pipeline):
        # type: (Pipeline) -> None
        super().__init__('RUNNING')
        self._pipeline = pipeline

    @property
    def pipeline(self):
        # type: () -> Pipeline
        return self._pipeline

    def wait_until_finish(self, duration=None):
        """
        等待 pipelines 运行结束,返回最终状态
        :param duration: 等待时间 (milliseconds). 若设置为 :data:`None`, 会无限等待
        :return: 最终的任务执行状态,或者 :data:`None` 表示超时
        """
        import asyncio

        loop = asyncio.get_event_loop()
        wait_task = loop.create_task(self.watch_job_status())
        return loop.run_until_complete(wait_task)

    async def watch_job_status(self):
        from ronds_sdk.tools.networkx_util import NetworkUtil

        failed_count = 0
        max_failed = 10
        graph = self.pipeline.graph

        while True:
            await asyncio.sleep(60 * 1)
            status = True
            failed_nodes = set()
            for node in NetworkUtil.dfs_postorder_nodes(graph):  # type: RayPhyTransform
                is_startup = await node.is_startup(max_retry=3)
                status = status and is_startup
                if not is_startup:
                    logger.warning("found breakdown node: %s" % node)
                    failed_nodes.add(node)
                    failed_count += 1
                    await node.startup()
                    logger.info("restart node: %s" % node)
            logger.info("job status: %s, failed_count: %d" % (status, failed_count))
            if status:
                failed_count = 0
            if failed_count >= max_failed:
                logger.error("job status error, restart failed too much: %s" % failed_nodes)
