import asyncio
import threading
import time
import traceback
from asyncio import exceptions, QueueEmpty
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING, List, Union, Optional, Tuple, Dict, Callable, Any

import ray
from ray.actor import ActorClass
from ray.remote_function import RemoteFunction
from ray.thirdparty_files import setproctitle
from retrying import retry

from ronds_sdk import logger_config, PipelineOptions, error
from ronds_sdk.options.pipeline_options import RayOptions
from ronds_sdk.tools import utils
from ronds_sdk.tools.constants import ExpandChainType, Constant, JobStatus
from ronds_sdk.tools.metaclass import MetaCollector
from ronds_sdk.tools.networkx_util import NetworkUtil
from ronds_sdk.tools.utils import async_retry
from ronds_sdk.transforms.ptransform import PTransform

if TYPE_CHECKING:
    from ronds_sdk.tools.buffer import MultiKeyBuffer
    from ray.util.placement_group import PlacementGroupSchedulingStrategy
    import networkx as nx

logger = logger_config.config()


class RayTransform(PTransform, metaclass=MetaCollector):

    def __init__(self,
                 worker_index,  # type: int
                 label=None,  # type: Optional[str]
                 timeout=10,  # type: int
                 maxsize=1000,  # type: int
                 fetch_size=1,  # type: int
                 parallel=None,  # type: Optional[int]
                 num_cpus=0.5,  # type: float
                 num_gpus=0,  # type: float
                 place_group=None,  # type: Optional[PlacementGroupSchedulingStrategy]
                 options=None,  # type: Optional[PipelineOptions]
                 is_merge=True,  # type: bool
                 ):
        """
        ray stream transform base class, suggest:
            - self property claimed in __init__ , assignment in pre_startup

        :param worker_index: required, worker instance index in ray cluster
        :param label: label
        :param timeout: timeout for process data, not used
        :param maxsize: max size records for buffer
        :param fetch_size: fetch size per batch
        :param parallel: worker parallel
        :param options: parameters for transform
        """
        super().__init__(label, parallel, options)
        self._num_cpus = num_cpus
        self._num_gpus = num_gpus
        self._place_group = place_group
        self._worker_index = worker_index
        self.timeout = timeout
        self.maxsize = maxsize
        self.fetch_size = fetch_size
        self._is_merge = is_merge

        self._expand_chain_type = ExpandChainType.ONE_TO_N
        self._job_status = JobStatus.INIT
        self._consuming = False
        self._receiving = False

        self.buffer = None  # type: Optional[MultiKeyBuffer]
        self.thread_pool = None  # type: Optional[ThreadPoolExecutor]
        self._ray_options = None  # type: Optional[RayOptions]
        self.child_transforms = None  # type: Optional[dict[str, List['RayTransform']]]
        self.parent_transforms = None  # type: Optional[dict[str, List['RayTransform']]]
        self._actor_name = None  # type: Optional[str]
        self._currents = None  # type: Optional[Dict[str, Any]]
        self._recv_selector = None  # type: Optional[Callable]

    def clone(self, worker_index):
        kwargs = dict(self.init_kwargs)
        kwargs['worker_index'] = worker_index
        instance = type(self)(*self.init_args, **kwargs)
        instance.pipeline = self.pipeline
        return instance

    @property
    def init_args(self):
        return getattr(self, '__init_args')

    @property
    def init_kwargs(self):
        return getattr(self, '__init_kwargs')

    @property
    def num_cpus(self):
        return self._num_cpus

    @property
    def num_gpus(self):
        return self._num_gpus

    @property
    def worker_index(self):
        return self._worker_index

    @property
    def is_merge(self):
        return self._is_merge

    @property
    def consumer_id(self):
        return self.label

    @property
    def ray_options(self):
        if self._ray_options is None:
            if self.options is not None:
                self._ray_options = self.options.view_as(RayOptions)
            elif self.pipeline is not None:
                self._ray_options = self.pipeline.options.view_as(RayOptions)
        return self._ray_options

    @property
    def expand_chain_type(self):
        return self._expand_chain_type

    @property
    def place_group(self):
        return self._place_group

    @place_group.setter
    def place_group(self, place_group):
        self._place_group = place_group

    @property
    def actor_name(self):
        if self._actor_name is None:
            self._actor_name = '%s_%d' % (utils.uid(), self.worker_index)
        return self._actor_name

    def _str_internal(self) -> str:
        name = super()._str_internal()
        if self.worker_index >= 0:
            name = '%s: %d' % (name, self.worker_index)
        return name

    def downstream(self) -> Dict[str, List['RayTransform']]:
        return self.child_transforms

    def keys(self):
        keys = set()
        if self.parent_transforms is not None:
            for _, pt in self.parent_transforms.items():
                for t in pt:
                    keys.add(t.consumer_id)
        return list(keys)

    def bind_downstream(self, name: str, pt: 'RayTransform'):
        if self.downstream() is None:
            self.child_transforms = dict()
        binds = self.downstream().setdefault(name, list())
        if pt not in binds:
            binds.append(pt)

    def bind_upstream(self, name: str, pt: 'RayTransform'):
        if self.parent_transforms is None:
            self.parent_transforms = dict()
        binds = self.parent_transforms.setdefault(name, list())
        if pt not in binds:
            binds.append(pt)

    def success(self):
        self._job_status = JobStatus.SUCCESS

    def failed(self, msg=None, e=None):
        self._job_status = JobStatus.FAILED
        if msg is not None:
            logger.error(msg)
        if e is not None:
            logger.error("record process failed: %s, %s" % (e, traceback.format_exc()))

    async def is_deployed(self):
        logger.info("%s: jobStatus: %s, tid: %s" % (self.label, self._job_status, threading.get_ident()))
        return self._job_status.v >= JobStatus.INIT.v

    async def is_startup(self):
        logger.info("%s: jobStatus: %s, tid: %s" % (self.label, self._job_status, threading.get_ident()))
        return self._job_status == JobStatus.SUCCESS

    def pre_startup(self):
        """
        在 __init__ 中声明属性， pre_startup 中进行初始化属性等操作
            - 防止出现 python 对象包含无法序列化的属性，导致序列化异常
            - ray 创建 worker 时无法通过已有对象创建，已有对象不要包含过多业务逻辑
        :return:
        """
        if self._job_status.v >= JobStatus.PREPARE.v:
            return
        self._job_status = JobStatus.PREPARE
        # relate transforms init
        if self.child_transforms is None:
            self.child_transforms = dict()
        if self.parent_transforms is None:
            self.parent_transforms = dict()
        # buffer init
        if self.buffer is None:
            from ronds_sdk.tools.buffer import MultiKeyBuffer
            keys = self.keys()
            logger.info("%s: parent keys: %s" % (str(self), keys))
            self.buffer = MultiKeyBuffer(maxsize=self.maxsize, keys=list(keys))
            self._currents = dict()
        if self._options is None and self.pipeline is not None:
            self._options = self.pipeline.options

    async def startup(self):
        """
        开启当前节点的数据读取和处理等流程
        :return: 常驻任务, 不结束, 无返回值
        """
        if self._job_status > JobStatus.INIT:
            logger.info("%s: already startup call, jobStatus: %s, worker: %s"
                        % (self.label, self._job_status, self.label))
            return
        self.pre_startup()
        if not self._consuming:
            asyncio.get_running_loop().create_task(self.consume())
            self._consuming = True
        logger.info("%s startup successfully, tid: %s ~" % (self.label, threading.get_ident()))
        self.success()

    async def fetch_currents(self, no_wait: bool = False) -> Optional[Dict[str, str]]:
        """
        load 远端数据到本地内存
        :return:
        """
        self._currents.clear()
        for p_name, queue in self.buffer.items():
            try:
                if no_wait:
                    try:
                        row_value = queue.get_nowait()
                    except QueueEmpty:
                        row_value = None
                else:
                    row_value = await queue.get()
                if row_value is not None:
                    self._currents[p_name] = row_value
            except exceptions.TimeoutError:
                logger.warning("no_wait: %d, label: %s" % (no_wait, self.label))

        return self._currents

    async def process(self, inputs):
        """
        自定义的数据处理流程, 默认依次返回第父节点的输出
        :param inputs: 一般为如下格式:

                        {
                            "parent_input_name_1": "input contents",
                            "parent_input__name_2": "input contents"
                        }

        :return:
        """
        for _, input_value in inputs.items():
            yield input_value

    async def consume(self):
        """
        从上游消费最新数据, 缓存到本地 buffer
        :return: 常驻任务, 不结束, 无返回值
        """
        while True:
            # noinspection PyBroadException
            try:
                start = time.time()
                current_dict = await self.fetch_currents()
                fetch_cost = time.time() - start
                if current_dict is None:
                    await asyncio.sleep(1)
                    continue
                results = self.process(current_dict)
                if results is None:
                    continue
                send_cost = 0
                async for r in results:
                    send_start = time.time()
                    await self.send(r)
                    send_cost += (time.time() - send_start)
                cost = time.time() - start
                if cost > Constant.COST_TIMEOUT.value:
                    logger.warning("%s: consume cost: %f, fetch_cost: %f, send_cost: %f}",
                                   str(self), cost, fetch_cost, send_cost)
                self.success()
            except Exception as ex:
                self.failed("consume failed, transform: %s, error: %s"
                            % (str(self), traceback.format_exc()), ex)

    # noinspection PyBroadException
    async def send(self, record):
        if record is None:
            return
        for _, receiver_instances in self.downstream().items():
            try:
                await self._send_selector(record, receiver_instances) \
                    .receive(self.consumer_id, record)
            except Exception:
                logger.error("send failed, transform: %s, error: %s"
                             % (str(self), traceback.format_exc()))

    async def receive(self, sender_id, records):
        # type: ('RayTransform', str, Union[str, List[str]]) -> None
        """
        存储收到的最新消息
        :param sender_id: 发送消息的组件 id
        :param records: 收到的最新数据
        :return: 最新数据
        """
        if self._job_status == JobStatus.INIT:
            logger.warning("%s: startup in receive, send_id: %s, tid: %s"
                           % (str(self), sender_id, threading.get_ident()))
            await self.startup()
        await self.buffer.key_put(sender_id, records)

    # noinspection PyMethodMayBeStatic
    def _send_selector(self, record: str, receiver_instances: List[PTransform]) -> 'RayTransform':
        if self._recv_selector is None:
            from ronds_sdk.tools import shuffle
            self._recv_selector = shuffle.recv_selector_strategy(record, receiver_instances)
            logger.info('%s: recv_selector_strategy: %s', str(self), self._recv_selector)

        return self._recv_selector(record, receiver_instances)


# noinspection PyArgumentList
@ray.remote(concurrency_groups={"io": 1, "request": 10})
class RayTransActor:
    def __init__(self, transform: 'RayTransform'):
        self._transform = transform
        setproctitle.setproctitle(transform.label)

    def __getattr__(self, item):
        if hasattr(self._transform, item):
            return getattr(self._transform, item)
        raise AttributeError

    def __str__(self):
        return self._transform.__str__()

    def __repr__(self):
        return self._transform.__repr__()

    @ray.method(concurrency_group='io')
    async def startup(self):
        logger.debug("startup thread id: %s" % threading.get_ident())
        await self._transform.startup()

    @ray.method(concurrency_group='request')
    async def is_startup(self):
        logger.debug("is_startup thread id: %s" % threading.get_ident())
        return await self._transform.is_startup()

    @ray.method(concurrency_group='request')
    async def is_deployed(self):
        return await self._transform.is_deployed()

    def downstream(self) -> Dict[str, List['RayTransform']]:
        return self._transform.downstream()

    def bind_downstream(self, name: str, pt):
        self._transform.bind_downstream(name, pt)

    def set_pipeline(self, p):
        """ for set_pipeline.remote() """
        self._transform.pipeline = p

    def actor_name(self):
        return self._transform.actor_name

    async def send(self, record):
        await self._transform.send(record)

    @ray.method(concurrency_group='io')
    async def receive(self, sender_id, records):
        await self._transform.receive(sender_id, records)


class RayPhyTransform(object):
    def __init__(self,
                 transform,  # type: 'RayTransform'
                 ):
        self._transform = transform
        self._remote_transform = None  # type: Optional[Union['ActorClass', 'RemoteFunction']]
        self._actor_name = self._transform.actor_name

    def __str__(self):
        return self._transform.__str__()

    def __repr__(self):
        return self._transform.__repr__()

    @property
    def remote_transform(self) -> Union['ActorClass', 'RemoteFunction']:
        return self._remote_transform

    @property
    def label(self):
        return self._transform.label

    @property
    def num_cpus(self):
        return self._transform.num_cpus

    @property
    def num_gpus(self):
        return self._transform.num_gpus

    @property
    def place_group(self):
        return self._transform.place_group

    @property
    def deployed(self):
        return self._remote_transform is not None

    @property
    def consumer_id(self):
        return self._transform.consumer_id

    def keys(self):
        return self._transform.keys()

    def actor_name(self):
        return self._actor_name

    def set_pipeline(self, p):
        self._transform.pipeline = p

    def bind_downstream(self, name: str, pt):
        self._transform.bind_downstream(name, pt)

    def bind_upstream(self, name: str, pt):
        self._transform.bind_upstream(name, pt)

    def _get_remote_transform(self, max_retry=10, timeout=10):
        logger.info("get actor: %s", self._actor_name)
        return retry(retry_on_result=lambda x: x is None,
                     wait_fixed=2 * timeout * 1000,
                     stop_max_attempt_number=max_retry,
                     stop_max_delay=120000)(ray.get_actor)(self._actor_name)

    async def receive(self, sender_id, records):
        """
        bind downstream by remote, receive will be called on remote node
        :param sender_id: sender id
        :param records: send records
        :return:
        """
        if self._remote_transform is None:
            self._remote_transform = self._get_remote_transform()
        await self._remote_transform.receive.remote(sender_id, records)

    async def startup(self):
        await self.remote_transform.startup.remote()

    async def _job_status(self, job_status):
        if job_status == JobStatus.INIT:
            return await self._remote_transform.is_deployed.remote()
        elif job_status == JobStatus.SUCCESS:
            return await self._remote_transform.is_startup.remote()

    async def is_startup(self, max_retry=100, timeout=10):
        try:
            return await async_retry(self._job_status,
                                     wait_fixed=2 * timeout * 1000,
                                     stop_max_attempt_number=max_retry,
                                     stop_max_delay=120000)(JobStatus.SUCCESS)
        except Exception as ex:
            logger.warning('%s: is_startup failed: %s, %s' % (str(self), str(ex), traceback.format_exc()))
            return False

    async def is_deployed(self, max_retry=100, timeout=10):
        return await async_retry(self._job_status,
                                 wait_fixed=2 * timeout * 1000,
                                 stop_max_attempt_number=max_retry,
                                 stop_max_delay=120000)(JobStatus.INIT)

    async def deploy(self) -> Union['ActorClass', 'RemoteFunction']:
        if self._remote_transform is None:
            self._remote_transform = RayTransActor \
                .options(name=self.actor_name(),
                         max_restarts=-1,
                         max_task_retries=3,
                         max_concurrency=1,
                         num_cpus=self.num_cpus,
                         num_gpus=self.num_gpus,
                         scheduling_strategy=self.place_group
                         ) \
                .remote(self._transform)
        logger.info("deploy %s: %s" % (self.label, self.actor_name()))
        if not await self.is_deployed():
            raise error.TransformError('deploy failed: %s' % str(self))
        return self._remote_transform


class StageRayTransform(RayTransform):
    def __init__(self,
                 graph,  # type: nx.DiGraph
                 worker_index=None,  # type: Optional[int]
                 ):
        """
        merge 1:1 Transform graph to a StageTransform
        :param graph: 1:1 Transform graph
        :param worker_index: transform worker index >= 0
        """
        self._graph = graph
        self._root_node = self.find_root_node()
        self._leaf_node = self.find_leaf_node()
        self.pipeline = self._root_node.pipeline
        if worker_index is None or worker_index < 0:
            worker_index = self._root_node.worker_index
        super().__init__(
            worker_index,
            self._chain_label(graph),
            self._root_node.timeout,
            self._root_node.maxsize,
            self._root_node.fetch_size,
            self._root_node.parallel,
            self._num_resources(graph, self._root_node)[0],
            self._num_resources(graph, self._root_node)[1],
            self._root_node.place_group,
            self._root_node.options,
            is_merge=False,
        )
        self._expand_chain_type = self._leaf_node.expand_chain_type

    def _chain_label(self,
                     graph,  # type: nx.DiGraph
                     ):
        # type: (...) -> str
        from ronds_sdk.tools.networkx_util import NetworkUtil
        label_list = [utils.bref_upper(node.label) for node in NetworkUtil.bfs_nodes(self._root_node, graph)]
        return "&".join(label_list)

    @property
    def consumer_id(self):
        """
        Receivers of StageRayTransform own the parent consumer id of the leaf node
        :return:
        """
        return self._leaf_node.consumer_id

    @staticmethod
    def _num_resources(graph,  # type: nx.DiGraph
                       root_node,  # type: RayTransform
                       ) -> Tuple[float, float]:
        from ronds_sdk.tools.networkx_util import NetworkUtil
        num_cpus = 0.0
        num_gpus = 0.0
        for node in NetworkUtil.bfs_nodes(root_node, graph):  # type: RayTransform
            num_cpus += node.num_cpus
            num_gpus += node.num_gpus
        if num_cpus > 1:
            num_cpus = round(num_cpus)
        if num_gpus > 1:
            num_gpus = round(num_gpus)
        return num_cpus, num_gpus

    def keys(self):
        return self._root_node.keys()

    def find_root_node(self) -> 'RayTransform':
        if self._graph is None:
            raise error.TransformError('graph is None!')
        root_nodes = list(NetworkUtil.get_root_nodes(self._graph))
        if len(root_nodes) != 1:
            raise error.TransformError('root node required unique, but found: %d' % len(root_nodes))
        root_node = root_nodes[0]
        assert isinstance(root_node, RayTransform)
        return root_node

    def find_leaf_node(self) -> 'RayTransform':
        if self._graph is None:
            raise error.TransformError('graph is None!')

        leaf_nodes = list(NetworkUtil.get_leaf_nodes(self._graph))
        if len(leaf_nodes) != 1:
            raise error.TransformError('root node required unique, but found: %d' % len(leaf_nodes))
        leaf_node = leaf_nodes[0]
        assert isinstance(leaf_node, RayTransform)
        return leaf_node

    def pre_startup(self):
        if self._job_status.v >= JobStatus.PREPARE.v:
            return
        self._job_status = JobStatus.PREPARE
        self._bind_stage_stream()

    async def startup(self):
        if self._job_status.v > JobStatus.INIT.v:
            logger.info("%s: jobStatus: %s, worker: %s"
                        % (self.label, self._job_status, self.label))
            return
        self.pre_startup()
        for node in NetworkUtil.bfs_nodes(self._root_node, self._graph):  # type: RayTransform
            await node.startup()
        self.success()

    async def is_startup(self):
        success_nodes = [node for node in NetworkUtil.bfs_nodes(self._root_node, self._graph)
                         if await node.is_startup()]
        logger.debug('is_startup: %d / %d'
                     % (len(success_nodes), self._graph.number_of_nodes()))
        return len(success_nodes) == self._graph.number_of_nodes()

    def _bind_stage_stream(self):
        """
        bind stream inner stage DAG that running in async loop
        :return: None
        """
        visited = set()
        for edge in self._graph.edges:
            if edge in visited:
                continue
            visited.add(edge)
            upstream = edge[0]  # type: RayTransform
            downstream = edge[1]  # type: RayTransform
            upstream.bind_downstream(downstream.label, downstream)
            downstream.bind_upstream(upstream.label, upstream)

    def bind_downstream(self, name, pt):
        super().bind_downstream(name, pt)
        self._leaf_node.bind_downstream(name, pt)

    def bind_upstream(self, name: str, pt):
        super().bind_upstream(name, pt)
        self._root_node.bind_upstream(name, pt)

    async def receive(self, sender_id, records):
        await self._root_node.receive(sender_id, records)
