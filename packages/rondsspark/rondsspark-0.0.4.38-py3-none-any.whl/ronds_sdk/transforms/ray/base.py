import asyncio
from asyncio import exceptions
from concurrent.futures import ThreadPoolExecutor

import ray
from ray.actor import ActorClass
from ray.remote_function import RemoteFunction

from ronds_sdk import logger_config, PipelineOptions, error
from ronds_sdk.options.pipeline_options import RayOptions
from ronds_sdk.transforms.ptransform import PTransform
from typing import TYPE_CHECKING, List, Union

if TYPE_CHECKING:
    from ronds_sdk.tools.buffer import MultiKeyBuffer

logger = logger_config.config()


class RayTransform(PTransform):

    def __init__(self,
                 worker_index,  # type: int
                 label=None,  # type: str
                 timeout=10,  # type: int
                 maxsize=100,  # type: int
                 fetch_size=1,  # type: int
                 parallel=1,  # type: int
                 options=PipelineOptions(),  # type: PipelineOptions
                 component=None,  # type: object
                 ):
        super().__init__(label)
        self._worker_index = worker_index
        # noinspection PyTypeChecker
        self.buffer = None  # type: MultiKeyBuffer
        # noinspection PyTypeChecker
        self.thread_pool = None  # type: ThreadPoolExecutor
        self.timeout = timeout
        self.maxsize = maxsize
        self.fetch_size = fetch_size
        self._parallel = parallel if parallel is not None else 1
        self._options = options
        self._ray_options = options.view_as(RayOptions)
        self.parent_transforms = []  # type: List[Union[RemoteFunction, ActorClass]]
        self._startup = False
        # noinspection PyTypeChecker
        self.current_refs = None  # type: List[ray.ObjectRef]

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__init_args = args
        instance.__init_kwargs = kwargs
        return instance

    @property
    def worker_index(self):
        return self._worker_index

    @property
    def consumer_id(self):
        return self.label

    @property
    def options(self):
        return self._options

    @property
    def ray_options(self):
        return self._ray_options

    @property
    def parallel(self):
        if self._parallel is not None:
            return self._parallel
        return self.ray_options.ray_parallel()

    def actor_name(self, worker_index=None):
        if worker_index is not None:
            return "%s_%d" % (self.label, worker_index)
        return self.label

    def buffer_pop(self, consumer_id, no_wait=False):
        return self.buffer.pop(consumer_id,
                               no_wait=no_wait,
                               fetch_size=self.fetch_size)

    def upstreams(self):
        # type: () -> List[Union[RemoteFunction, ActorClass]]
        return self.parent_transforms

    def bind_upstreams(self, name, pt):
        self.parent_transforms.append(pt)
        self.parent_names.append(name)

    async def is_startup(self):
        return self._startup & await self.is_startup_parent()

    async def is_startup_parent(self):
        while True:
            logger.debug("check parent startup ?")
            started = True
            for pt in self.upstreams():
                # noinspection PyUnresolvedReferences
                started = started & await pt.is_startup.remote()
            if not started:
                logger.debug("startup not finished !")
                await asyncio.sleep(1)
            else:
                logger.debug("startup done ~")
                return True

    def _prepare_fetch_currents(self, no_wait=False):
        """
        异步触发远端数据的读取, 获取数据的 ref
        :return: 
        """
        self.current_refs.clear()
        for pt in self.upstreams():
            # noinspection PyUnresolvedReferences
            self.current_refs.append(pt.next.remote(self.consumer_id, no_wait))

    async def fetch_currents(self, no_wait=False):
        # type: (int) -> Union[dict[str, str], None]
        """
        load 远端数据到本地内存
        :return:
        """
        if self.current_refs is None:
            self.current_refs = list()
            self._prepare_fetch_currents(no_wait)
        current_dict = None
        for i, row in enumerate(self.current_refs):
            try:
                p_name = self.parent_names[i]
                row_value = await row
                if row_value is not None:
                    if current_dict is None:
                        current_dict = dict()
                    current_dict[p_name] = row_value
            except exceptions.TimeoutError:
                logger.debug("no_wait: %d, label: %s" % (no_wait, self.label))

        self._prepare_fetch_currents(no_wait)
        return current_dict

    async def startup(self):
        """
        开启当前节点的数据读取和处理等流程
        :return: 常驻任务, 不结束, 无返回值
        """
        if self._startup:
            logger.info("%s already startup" % self.actor_name(self.worker_index))
            return
        logger.info("startup parent size: %d" % len(self.upstreams()))
        for pt in self.upstreams():
            # noinspection PyUnresolvedReferences
            pt.startup.remote()
        if self.buffer is None:
            from ronds_sdk.tools.buffer import MultiKeyBuffer
            self.buffer = MultiKeyBuffer(maxsize=self.maxsize)
        if await self.is_startup_parent():
            self._startup = True
            logger.info("%s startup successfully ~" % self.actor_name(self.worker_index))
            await self.consume()

    async def consume(self):
        """
        从上游消费最新数据, 缓存到本地 buffer
        :return: 常驻任务, 不结束, 无返回值
        """
        while True:
            logger.debug("consume next start, current_refs if None: %s"
                         % (self.current_refs is None))
            current_dict = await self.fetch_currents()
            if current_dict is None:
                await asyncio.sleep(0.5)
                continue
            results = self.process(current_dict)
            if results is None:
                await asyncio.sleep(0)
                continue
            for res in results:
                logger.debug("consume res: %s" % res)
                await self.buffer.put(res)

    async def next(self, consumer_id, no_wait=False):
        """
        下游读取当前节点处理完成的最新数据
        :param consumer_id: 下游节点的消费 id
        :param no_wait: no_wait
        :return: 最新数据
        """
        return await self.buffer_pop(consumer_id, no_wait)

    def process(self, inputs):
        # type: (dict[str, Union[str, List[str]]]) -> Union[str, List[str], None]
        """
        自定义的数据处理流程, 默认依次返回第父节点的输出
        :param inputs: 一般为如下格式:

                        {
                            "parent_input_name_1": "input contents",
                            "parent_input__name_2": "input contents"
                        }

        :return:
        """
        for input_name, input_value in inputs.items():
            yield input_value

    def deploy(self, upstreams=None, parallel=None):
        # type: (list[Union[ActorClass, RemoteFunction]], int) -> list[Union[ActorClass, RemoteFunction]]

        worker_list = list()
        parallel = parallel if parallel is not None else self._parallel
        if parallel is None:
            raise error.TransformError("parallel must not None!")
        self._parallel = parallel
        self.__init_kwargs['parallel'] = parallel
        # create ray workers
        for i in range(parallel):
            self.__init_kwargs['worker_index'] = i
            f_remote = ray.remote(type(self))
            f_actor_handle = f_remote.remote(*self.__init_args, **self.__init_kwargs)
            worker_list.append(f_actor_handle)

        # bind upstream
        if upstreams is not None:
            wait_handle = list()
            max_parallel = max(parallel, len(upstreams))
            for i in range(max_parallel):
                f_actor_handle = worker_list[i % parallel]
                upstream_actor_handle = upstreams[i % len(upstreams)]
                actor_name = ray.get(upstream_actor_handle.actor_name.remote(i % len(upstreams)))
                bind_handle = f_actor_handle.bind_upstreams.remote(actor_name, upstream_actor_handle)
                wait_handle.append(bind_handle)
            ray.get(wait_handle)
        return worker_list
