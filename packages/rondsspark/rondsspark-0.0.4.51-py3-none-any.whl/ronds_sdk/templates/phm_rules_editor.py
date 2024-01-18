import os
import sys

from ronds_sdk.tools.utils import GraphParser, RuleParser, to_bool


# noinspection PyUnusedLocal
def run(rule_path: str,
        alg_path: str,
        alg_func: str,
        graph_path: str,
        spark_master_url: str = None,
        start_time: str = None,
        send_kafka_mock: bool = False):
    import ronds_sdk as ronds
    sys.path.append(alg_path)
    # init params
    graph_parser = GraphParser(graph_path)
    rule_parser = RuleParser(rule_path)
    rules = rule_parser.load()
    spark_repartition_num = 1
    options = ronds.Options(
        enable_executor_debug=to_bool(os.getenv('EXECUTOR_DEBUG', False)),
        # spark
        transform_package='ronds_sdk.transforms.pandas.transforms',
        spark_repartition_num=spark_repartition_num,
        spark_master_url=spark_master_url,
        # algorithm
        algorithm_path=alg_path,
        algorithm_funcname=alg_func,
        # cassandra
        # cassandra_start_datetime="2022-04-29 12:12:37",
        cassandra_start_datetime=graph_parser.start_time(),
        cassandra_host=graph_parser.cassandra_host(),
        cassandra_keyspace=graph_parser.cassandra_keyspace(),
        cassandra_table_process=graph_parser.cassandra_process_table(),
        cassandra_table_index=graph_parser.cassandra_index_table(),
        # cassandra window
        process_data_window_duration=graph_parser.process_window_duration(),
        index_data_window_duration=graph_parser.index_window_duration(),
        index_data_slide_duration=graph_parser.index_slide_duration(),
        # kafka
        kafka_bootstrap_servers=graph_parser.kafka_bootstraps(),
        kafka_send_mock=send_kafka_mock,
    )
    # create and run pipeline
    with ronds.Pipeline(options=options) as p:
        p | 'Rule Cassandra Scan' >> ronds.RulesCassandraScan(rules) \
            | 'algorithm' >> ronds.Algorithm() \
            | 'send algorithm json kafka' >> ronds.SendAlgJsonKafka(graph_parser.kafka_source_topics())
