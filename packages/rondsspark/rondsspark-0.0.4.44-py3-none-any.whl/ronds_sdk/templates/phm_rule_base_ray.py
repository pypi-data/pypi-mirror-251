import os
import sys

from ronds_sdk import logger_config
from ronds_sdk.parser.arg_parser import RuleBaseArgParser
from ronds_sdk.tools.constants import JsonKey
from ronds_sdk.tools.utils import to_bool
from ronds_sdk.transforms.ray.streaming.algorithm import RuleBaseAlgorithm
from ronds_sdk.transforms.ray.streaming.kafka import KafkaReader, KafkaAlgSender
from ronds_sdk.transforms.ray.streaming.redis import RuleReadRedisBuffer, RuleSaveRedisBuffer

logger = logger_config.config()


# noinspection PyUnusedLocal
def run(rule_path,
        alg_path,
        alg_func,
        graph_path,
        spark_master_url=None,
        start_time=None,
        send_kafka_mock=False,
        parallel=4
        ):
    sys.path.append(alg_path)
    # init params
    arg_parser = RuleBaseArgParser(graph_path)
    kafka_topics = arg_parser.save_kafka_topics()
    reader_topics = ['graph_sh_indices_json_B']  # arg_parser.kafka_reader_topic()['topics']
    alg_config = arg_parser.algorithm_config()
    reader_group_id = arg_parser.kafka_group_id()
    worker_flow_id = arg_parser.get_worker_flow_id

    import ronds_sdk as ronds
    options = ronds.Options(
        enable_executor_debug=to_bool(os.getenv('EXECUTOR_DEBUG', False)),
        # algorithm
        algorithm_path=alg_path,
        algorithm_funcname=alg_func,
        # kafka
        kafka_bootstrap_servers='172.16.3.51,172.16.3.52,172.16.3.53',
        kafka_send_mock=send_kafka_mock,
        kafka_group_id=reader_group_id,
        kafka_auto_offset_reset='largest',
        # redis
        redis_host="172.16.0.112",
        redis_port=7000,
        redis_password="redis123",
        redis_username="default",
    )

    from ronds_sdk.runners.ray_runner import RayStreamRunner
    from ronds_sdk import Pipeline
    schema = (
        (JsonKey.ID.value, str),
        (JsonKey.MESSAGE.value, dict),
        ('topic', str),
        ('arrive_time', int),
        ('partition', int),
        ('offset', int),
    )
    with Pipeline(namespace=worker_flow_id, options=options, runner=RayStreamRunner) as p:
        p | 'KafkaReader' >> KafkaReader(reader_topics, schema=schema, parallel=parallel) \
            | "RuleReadRedisBuffer" >> RuleReadRedisBuffer(p.namespace) \
            | "RuleBaseAlgorithm" >> RuleBaseAlgorithm(alg_config) \
            | "RuleSaveRedisBuffer" >> RuleSaveRedisBuffer() \
            | "KafkaAlgSender" >> KafkaAlgSender(kafka_topics)
