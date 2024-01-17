import traceback
from typing import TYPE_CHECKING, List, Optional, cast, Set, Tuple

import ray
from networkx import DiGraph
from ray.util.placement_group import placement_group

from ronds_sdk import error, logger_config
from ronds_sdk.options.pipeline_options import RayOptions
from ronds_sdk.runners.planners import PipeRule, ExpandedPipeRule
from ronds_sdk.tools import utils
from ronds_sdk.tools.constants import ExpandChainType
from ronds_sdk.tools.networkx_util import NetworkUtil
from ronds_sdk.transforms.ptransform import ChainedPTransform

if TYPE_CHECKING:
    from ronds_sdk import Pipeline
    from ronds_sdk.transforms.ptransform import PTransform
    from ronds_sdk.transforms.ray.base import RayTransform
    from ray.util.scheduling_strategies import PlacementGroupSchedulingStrategy

__all__ = [
    'RayStreamConvertRule',
    'RayStreamPhysicalRule',
    'RayPlacementGroupRule',
]

logger = logger_config.config()


class RayStreamConvertRule(PipeRule):
    """
    Graph logical node expand to parallel stream worker nodes
    """

    def on_match(self, transform, pipeline):
        from ronds_sdk.transforms.ray.base import RayTransform
        if not isinstance(transform, RayTransform):
            raise error.PlannerError('invalid ray transform: [%s]' % transform)
        ray_options = pipeline.options.view_as(RayOptions)
        default_parallel = ray_options.parallel()
        parallel = max(default_parallel, transform.parallel or 1)
        worker_list = []
        for i in range(parallel):
            worker_list.append(transform.clone(i))
        return ChainedPTransform(*worker_list, label=transform.label)

    def apply(self, pipeline):
        # type: ('RayStreamConvertRule', Pipeline) -> Pipeline
        pipeline = super().apply(pipeline)
        return self.expand_chained(pipeline)

    def expand_chained(self, pipeline):
        # type: ('RayStreamConvertRule', Pipeline) -> Pipeline
        from ronds_sdk import Pipeline
        phy_pipeline = Pipeline(pipeline.options, argv=None, runner=pipeline.runner)
        expanded = set()
        for edge in pipeline.edges():
            up_node = edge[0]
            down_node = edge[1]
            if not isinstance(up_node, ChainedPTransform) \
                    or not isinstance(down_node, ChainedPTransform):
                raise error.PlannerError('invalid chained node: [%s, %s]' % (up_node, down_node))
            if edge in expanded:
                continue
            expanded.add(edge)
            if utils.collection_empty(up_node.parts) \
                    or utils.collection_empty(down_node.parts):
                continue
            if up_node.parts[0].expand_chain_type == ExpandChainType.ONE_TO_ALL:
                self._one_to_all(up_node, down_node, phy_pipeline)
            else:
                self._some_to_some(up_node, down_node, phy_pipeline)
        pipeline.graph = phy_pipeline.graph
        pipeline.expand = True
        return pipeline

    @staticmethod
    def _some_to_some(up_node, down_node, phy_pipeline):
        max_node_num = max(len(up_node.parts), len(down_node.parts))
        for i in range(max_node_num):
            up_remote = up_node.parts[i % len(up_node.parts)]
            down_remote = down_node.parts[i % len(down_node.parts)]
            phy_pipeline.add_edge(up_remote, down_remote)

    @staticmethod
    def _one_to_all(up_node, down_node, phy_pipeline):
        for up in up_node.parts:
            for down in down_node.parts:
                phy_pipeline.add_edge(up, down)


class RayStreamPhysicalRule(ExpandedPipeRule):
    """
    Graph logical node transform to physical node, apply rules after ray.init()
    """

    def on_match(self, transform, pipeline):
        # type: ('RayStreamPhysicalRule', PTransform, Pipeline) -> 'RayTransform'
        from ronds_sdk.transforms.ray.base import RayTransform, RayPhyTransform
        assert isinstance(transform, RayTransform)
        rpt = RayPhyTransform(transform)
        rpt.set_pipeline(pipeline)
        return cast(RayTransform, rpt)


class RayPlacementGroupRule(ExpandedPipeRule):

    MAX_BUNDLE_NUM = 30

    def __init__(self):
        self.bundle_visited = set()

    def apply(self, pipeline):
        # type: ('RayPlacementGroupRule', Pipeline) -> Pipeline
        self._apply_sub(NetworkUtil.get_root_nodes(pipeline.graph), pipeline)
        self._apply_sub(self._one_to_all_sub_nodes(pipeline.graph), pipeline)
        return pipeline

    def _apply_sub(self, root_nodes, pipeline):
        from ronds_sdk.transforms.ray.base import RayTransform
        try:
            for root_node in root_nodes:
                assert isinstance(root_node, RayTransform)
                nodes, bundles = self._sub_tree_bundles(root_node, pipeline)
                if len(bundles) > RayPlacementGroupRule.MAX_BUNDLE_NUM or len(bundles) <= 1:
                    continue
                pg = self._require_pg(bundles)
                if pg is not None:
                    self._attach_pg_strategy(nodes, pg)
        except Exception as ex:
            logger.error('Failed to get placement group: %s, \n%s', ex, traceback.format_exc())
            raise error.PlannerRuleError('Failed to get placement group: %s, \n%s'
                                         % (ex, traceback.format_exc()))

    @staticmethod
    def _one_to_all_sub_nodes(graph):
        # type: (DiGraph) -> set
        nodes = set()
        for node in graph.nodes:
            if node.expand_chain_type == ExpandChainType.ONE_TO_ALL:
                for sn in graph.successors(node):
                    nodes.add(sn)
        return nodes

    def _sub_tree_bundles(self, root_node, pipeline):
        # type: ('RayPlacementGroupRule', RayTransform, Pipeline) -> Tuple[Set, List[dict]]
        bundles = []
        graph = pipeline.graph
        nodes = set()
        for node in NetworkUtil.bfs_nodes(root_node, graph, self._successor_match):
            if node.expand_chain_type != ExpandChainType.ONE_TO_ALL:
                bundles.append({
                    'CPU': node.num_cpus,
                    'GPU': node.num_gpus,
                })
                nodes.add(node)
            self.bundle_visited.add(node)
        return nodes, bundles

    def _successor_match(self, s: 'RayTransform') -> bool:
        from ronds_sdk.transforms.ray.base import RayTransform
        assert isinstance(s, RayTransform)
        if s in self.bundle_visited:
            return False
        self.bundle_visited.add(s)
        return s.expand_chain_type != ExpandChainType.ONE_TO_ALL

    @staticmethod
    def _attach_pg_strategy(nodes, pg):
        for node in nodes:
            if node.place_group is None:
                node.place_group = pg

    @staticmethod
    def _require_pg(bundles):
        # type: (List[dict]) -> Optional[PlacementGroupSchedulingStrategy]
        if utils.collection_empty(bundles):
            return None
        pending_pg = placement_group(bundles, strategy="PACK")
        try:
            from ray.util.scheduling_strategies import PlacementGroupSchedulingStrategy
            ray.get(pending_pg.ready(), timeout=10)
            return PlacementGroupSchedulingStrategy(
                placement_group=pending_pg,
            )
        except Exception as ex:
            logger.warning("Failed to get placement group: %s,\n%s",
                           ex, traceback.format_exc())
        return None
