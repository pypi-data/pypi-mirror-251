import os
import sys
import threading

import ray

from ronds_sdk.options.pipeline_options import KafkaOptions
from ronds_sdk.tools.constants import JsonKey
from ronds_sdk.tools.utils import GraphParser, RuleParser, to_bool
from ronds_sdk.transforms.ray.streaming.algorithm import RuleAlgorithm
from ronds_sdk.transforms.ray.streaming.filter import FilterByPhmRules
from ronds_sdk.transforms.ray.streaming.kafka import KafkaReader, KafkaAlgSender
from ronds_sdk.transforms.ray.streaming.shuffle import Shuffle


def run(rule_path,
        alg_path,
        alg_func,
        graph_path,
        spark_master_url=None,
        start_time=None,
        send_kafka_mock=False):
    sys.path.append(alg_path)
    # init params
    graph_parser = GraphParser(graph_path)
    rule_parser = RuleParser(rule_path)
    rules = rule_parser.load()
    kafka_topics = graph_parser.kafka_source_topics()
    reader_topics = graph_parser.kafka_reader_topic()['topics']
    parallel_num = len(rules) if len(rules) < 1000 else 1000

    import ronds_sdk as ronds
    options = ronds.Options(
        enable_executor_debug=to_bool(os.getenv('EXECUTOR_DEBUG', False)),
        # algorithm
        algorithm_path=alg_path,
        algorithm_funcname=alg_func,
        algorithm_window_duration=graph_parser.window_duration(),
        algorithm_window_slide_duration=graph_parser.window_slide_window(),
        # kafka
        kafka_bootstrap_servers=graph_parser.kafka_bootstraps(),
        kafka_send_mock=send_kafka_mock,
    )

    ray.init()
    nodes = ray.nodes()
    # kafka reader
    kafka_reader_parallel = min(len(nodes), parallel_num)
    kafka_readers = KafkaReader(reader_topics, options.view_as(KafkaOptions))\
        .deploy(parallel=kafka_reader_parallel)

    # filter by phm rules
    parallel_num = parallel_num
    filter_list = FilterByPhmRules(rules) \
        .deploy(kafka_readers, parallel=parallel_num)

    # shuffle by rule id
    shuffle_list = Shuffle(JsonKey.RULE_GROUP.value) \
        .deploy(filter_list, parallel=parallel_num)

    # algorithm process
    algorithm_list = RuleAlgorithm(rules, options, dt_column='Time') \
        .deploy(shuffle_list, parallel=parallel_num)

    # result send alter event
    kafka_alg_sender_list = KafkaAlgSender(kafka_topics, options) \
        .deploy(algorithm_list, parallel=parallel_num)

    # startup
    for kafka_sender in kafka_alg_sender_list:
        kafka_sender.startup.remote()
    threading.Event().wait()
