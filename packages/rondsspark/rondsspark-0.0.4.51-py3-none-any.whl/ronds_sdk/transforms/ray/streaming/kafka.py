import datetime
import traceback
from typing import List, Optional
from typing import TYPE_CHECKING

import aiokafka
import ujson
from aiokafka import ConsumerRecord

from ronds_sdk import logger_config
from ronds_sdk.datasources.kafka_manager import KafkaManager
from ronds_sdk.models.message import Message
from ronds_sdk.options.pipeline_options import KafkaOptions
from ronds_sdk.tools import utils
from ronds_sdk.tools.constants import Parallel, JsonKey
from ronds_sdk.transforms import ronds
from ronds_sdk.transforms.pandas.transforms import SendAlgJsonKafka
from ronds_sdk.transforms.ray.base import RayTransform

if TYPE_CHECKING:
    from ronds_sdk import PipelineOptions

logger = logger_config.config()


class KafkaReader(RayTransform):
    """
    Kafka 循环读取数据
    kafka 读取数据完整的 schema:
        (
            ('id', str),
            ('_message', dict),
            ('topic', str),
            ('arrive_time', int),
            ('partition', int),
            ('offset', int),
        )
    按顺序依次指定，可设置 None 或者从后截断
    """

    def __init__(self,
                 topics,  # type: List[str]
                 options=None,  # type: Optional[PipelineOptions]
                 parallel=None,  # type: Optional[int]
                 num_cpus=0.5,  # type: float
                 num_gpus=0,  # type: float
                 worker_index=-1,  # type: int
                 schema=None,
                 ):
        super().__init__(worker_index,
                         parallel=parallel or Parallel.WORKER_NUM.value,
                         num_cpus=num_cpus,
                         num_gpus=num_gpus,
                         options=options)
        self.topics = topics
        self.schema = schema or (
            (JsonKey.ID.value, str),
            (JsonKey.MESSAGE.value, dict),
        )

    def _assigns(self, consumer):
        # noinspection PyPackageRequirements,PyProtectedMember
        from kafka import TopicPartition
        assigns = []
        for topic in self.topics:
            partitions = consumer.partitions_for_topic(topic)
            for partition in partitions:
                assert isinstance(partition, int)
                if utils.hash_md5(partition) % self.parallel == self.worker_index:
                    assigns.append(TopicPartition(topic, partition))
                    logger.info('Assign topic: %s, partition: %s', topic, partition)
        return assigns

    async def consume(self):
        _kafka_options = self.options.view_as(KafkaOptions)
        kafka_servers = _kafka_options.bootstrap_servers()
        reset = _kafka_options.auto_offset_reset()

        consumer = aiokafka.AIOKafkaConsumer(
            bootstrap_servers=kafka_servers,
            group_id=_kafka_options.group_id(),
            enable_auto_commit=False,
            auto_offset_reset=reset,
        )
        logger.info("bootstrap_servers: %s, group_id: %s, auto_offset_reset: %s",
                    kafka_servers, _kafka_options.group_id(), reset)
        await consumer.start()
        assigns = self._assigns(consumer)
        if len(assigns) > 0:
            consumer.assign(assigns)
            while True:
                try:
                    result = await consumer.getmany(timeout_ms=5 * 1000)
                    for tp, msgs in result.items():
                        if msgs:
                            await self.batch_process(msgs)
                            await consumer.commit({tp: msgs[-1].offset + 1})
                    self.success()
                except Exception as ex:
                    self.failed("consume error: %s" % traceback.format_exc(), ex)
                    logger.error("consume error: %s", traceback.format_exc())

    async def batch_process(self, messages: 'List[ConsumerRecord]'):
        for msg in messages:
            msg_str = self._schema_msg(msg)
            await self.send(msg_str)

    def _schema_msg(self, message: 'aiokafka.ConsumerRecord') -> str:
        if self.schema is None:
            # noinspection PyArgumentList
            return message.value().decode('utf-8')
        return ujson.dumps(self.set_message(message))

    @staticmethod
    def set_message(message: 'ConsumerRecord') -> Message:
        msg: Message = {
            'id': message.key.decode('utf-8') if message.key else '',
            '_message': ujson.loads(message.value.decode('utf-8')),
            'topic': message.topic,
            'arrive_time': datetime.datetime.fromtimestamp(int(message.timestamp / 1000))
            .strftime("%Y-%m-%dT%H:%M:%S"),
            'partition': int(message.partition),
            'offset': int(message.offset),
        }
        return msg


class KafkaAlgSender(RayTransform):
    def __init__(self,
                 kafka_sources,  # type: dict
                 options=None,  # type: Optional[PipelineOptions]
                 parallel=None,  # type: Optional[int]
                 num_cpus=0.5,  # type: float
                 num_gpus=0,  # type: float
                 worker_index=-1,  # type: int
                 ):
        super().__init__(worker_index,
                         parallel=parallel,
                         num_cpus=num_cpus,
                         num_gpus=num_gpus,
                         options=options)
        self.kafka_sources = kafka_sources
        self.send_alg_json_kafka = None  # type: Optional[SendAlgJsonKafka]

    def pre_startup(self):
        super().pre_startup()
        self.send_alg_json_kafka = SendAlgJsonKafka(ronds.SendAlgJsonKafka(self.kafka_sources),
                                                    self.options)

    async def process(self, inputs):
        input_json_list = list()
        for p_name, record in inputs.items():

            if isinstance(record, list):
                for r in record:
                    r_obj = ujson.loads(r)
                    input_json_list.append(r_obj)
            else:
                r_obj = ujson.loads(record)
                input_json_list.append(r_obj)
            yield record
        await self.send_alg_json_kafka.send_df(input_json_list)


class KafkaSender(RayTransform):
    def __init__(self,
                 kafka_source,  # type: dict
                 options=None,  # type: Optional[PipelineOptions]
                 parallel=None,  # type: Optional[int]
                 num_cpus=0.5,  # type: float
                 num_gpus=0,  # type: float
                 worker_index=-1,  # type: int
                 ):
        super().__init__(worker_index,
                         parallel=parallel,
                         num_cpus=num_cpus,
                         num_gpus=num_gpus,
                         options=options)
        self.kafka_source = kafka_source
        self.kafka_manager = None  # type: Optional[KafkaManager]
        self.topics = self.kafka_source['topics']

    def pre_startup(self):
        super().pre_startup()
        bootstraps = self.kafka_source['bootstraps']  # type: str
        kafka_port = self.kafka_source['port']  # type: int
        kafka_servers = ','.join(['%s:%s' % (s, kafka_port) for s in bootstraps.split(',')])
        self.kafka_manager = KafkaManager(kafka_servers)

    async def process(self, inputs):
        input_json_list = list()
        for record in inputs.values():
            kafka_msg = ujson.loads(record)
            if isinstance(kafka_msg, list):
                for r in kafka_msg:
                    input_json_list.append(r)
            else:
                input_json_list.append(kafka_msg)
            yield record
        await self.send_kafka(input_json_list)

    async def send_kafka(self, input_json_list):
        for record in input_json_list:
            if JsonKey.ID.value in record and JsonKey.MESSAGE.value in record:
                for topic in self.topics:
                    await self.kafka_manager.send(topic, record[JsonKey.ID.value],
                                                  ujson.dumps(record[JsonKey.MESSAGE.value]))
