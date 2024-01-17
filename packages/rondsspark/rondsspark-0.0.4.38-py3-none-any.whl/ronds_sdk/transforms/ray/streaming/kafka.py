import asyncio
import json
from typing import List, Union
import ray
from typing import TYPE_CHECKING
import pandas as pd

from ronds_sdk import logger_config
from ronds_sdk.options.pipeline_options import KafkaOptions

from ronds_sdk.transforms import ronds
from ronds_sdk.transforms.pandas.transforms import SendAlgJsonKafka
from ronds_sdk.transforms.ray.base import RayTransform

if TYPE_CHECKING:
    pass

logger = logger_config.config()


class KafkaReader(RayTransform):
    """
    Kafka 循环读取数据
    """
    def __init__(self, topics, options, parallel=None, worker_index=-1):
        # type: (List[str], KafkaOptions, int, int) -> None
        super().__init__(worker_index, parallel=parallel)
        self._options = options
        self.kafka_servers = options.kafka_bootstrap_servers
        self.topics = topics
        self.conf = {
            'bootstrap.servers': self.kafka_servers,
            'group.id': "f1",
            'session.timeout.ms': 6000,
            'enable.auto.commit': True,  # 把自动提交打开
            # 'default.topic.config': {'auto.offset.reset': 'smallest'},
        }

    async def consume(self):
        from confluent_kafka import Consumer, KafkaException
        consumer = Consumer(self.conf)
        consumer.subscribe(self.topics)
        try:
            while True:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    await asyncio.sleep(0.5)
                    continue
                if msg.error():
                    raise KafkaException(msg.error())
                # noinspection PyArgumentList
                msg_str = msg.value().decode('utf-8')
                await self.buffer.put(msg_str)
        finally:
            consumer.close()


class KafkaAlgSender(RayTransform):
    def __init__(self, topics, options, parallel=None, worker_index=-1):
        super().__init__(worker_index, parallel=parallel)
        self.send_alg_json_kafka = SendAlgJsonKafka(ronds.SendAlgJsonKafka(topics), options)

    def process(self, inputs):
        # type: (dict[str, Union[str, List[str]]]) -> Union[str, List[str], None]
        input_json_list = list()
        for record in inputs.values():
            if isinstance(record, list):
                for r in record:
                    input_json_list.append(json.loads(r))
            else:
                input_json_list.append(json.loads(record))
        self.send_kafka(input_json_list)
        return None

    def send_kafka(self, records):
        # type: (list[dict]) -> None
        df = pd.DataFrame(records)
        self.send_alg_json_kafka.send_df(df)
