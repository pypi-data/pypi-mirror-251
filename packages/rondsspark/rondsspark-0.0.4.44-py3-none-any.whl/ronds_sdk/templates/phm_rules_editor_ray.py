import os
import sys
from typing import TYPE_CHECKING

from ronds_sdk import logger_config
from ronds_sdk.parser.arg_parser import EditorArgParser
from ronds_sdk.parser.rule_parser import EditorRuleParser
from ronds_sdk.tools.constants import JsonKey
from ronds_sdk.tools.utils import to_bool
from ronds_sdk.transforms.ray.streaming.algorithm import RuleWindowAlgorithm
from ronds_sdk.transforms.ray.streaming.filter import FilterByPhmRules
from ronds_sdk.transforms.ray.streaming.kafka import KafkaReader, KafkaAlgSender
from ronds_sdk.transforms.ray.streaming.shuffle import Shuffle

if TYPE_CHECKING:
    from ronds_sdk import Pipeline

logger = logger_config.config()


def pipeline(rule_path,
             alg_path,
             alg_func,
             graph_path,
             send_kafka_mock=False,
             parallel_num=10
             ) -> 'Pipeline':
    from ronds_sdk.runners.ray_runner import RayStreamRunner
    from ronds_sdk import Pipeline

    # init params
    arg_parser = EditorArgParser(graph_path)
    rule_parser = EditorRuleParser(rule_path)
    rules = rule_parser.load()
    kafka_topics = arg_parser.save_kafka_topics()
    reader_topics = arg_parser.kafka_reader_topic()['topics']
    reader_group_id = arg_parser.kafka_group_id()
    parallel_num = min(len(rules), parallel_num)
    worker_flow_id = arg_parser.get_worker_flow_id

    import ronds_sdk as ronds
    options = ronds.Options(
        enable_executor_debug=to_bool(os.getenv('EXECUTOR_DEBUG', False)),
        # algorithm
        algorithm_path=alg_path,
        algorithm_funcname=alg_func,
        algorithm_window_duration=arg_parser.window_duration(),
        algorithm_window_slide_duration=arg_parser.window_slide_window(),
        # kafka
        kafka_bootstrap_servers=arg_parser.kafka_bootstraps(),
        kafka_send_mock=send_kafka_mock,
        kafka_group_id=reader_group_id,
        kafka_auto_offset_reset='largest',
    )
    p = Pipeline(namespace=worker_flow_id, options=options, runner=RayStreamRunner)
    p | 'KafkaReader' >> KafkaReader(reader_topics) \
        | "rule filter" >> FilterByPhmRules(rules, parallel=parallel_num) \
        | "Shuffle" >> Shuffle(JsonKey.RULE_GROUP.value) \
        | "algorithm" >> RuleWindowAlgorithm(rules, dt_column='Time') \
        | "kafka sender" >> KafkaAlgSender(kafka_topics)
    return p


# noinspection PyUnusedLocal
def run(rule_path,
        alg_path,
        alg_func,
        graph_path,
        spark_master_url=None,
        start_time=None,
        send_kafka_mock=False):
    if alg_path not in sys.path:
        sys.path.append(alg_path)
    p = pipeline(rule_path, alg_path, alg_func, graph_path, send_kafka_mock)
    p.run().wait_until_finish()
