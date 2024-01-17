from datetime import date, datetime

import findspark

import ronds_sdk.transforms.ronds as ronds
from ronds_sdk.options.pipeline_options import PipelineOptions
from ronds_sdk.pipeline import Pipeline

findspark.init()


def mock_data():
    """离线模拟数据"""
    return [(1, 2., 'string1', date(2000, 1, 1), datetime(2000, 1, 1, 12, 0)),
            (2, 3., 'string2', date(2000, 2, 1), datetime(2000, 1, 2, 12, 0)),
            (3, 4., 'string3', date(2000, 3, 1), datetime(2000, 1, 3, 12, 0))]


def test_create():
    """创建离线数据处理流程"""
    with Pipeline() as pipeline:
        pipeline | "Create elements" >> ronds.Create(mock_data()) \
            | "Filter elements" >> ronds.Filter("_1", "_1 > '1'") \
            | "console" >> ronds.Console()


def test_socket():
    """创建实时数据流处理流程"""
    with Pipeline() as pipeline:
        pipeline | "Create Socket" >> ronds.Socket("localhost", 9999) \
            | "Filter elements" >> ronds.Filter("value", "value is not null") \
            | "console" >> ronds.Console('append')


def test_socket_multi():
    """创建实时数据流处理流程"""
    with Pipeline() as pipeline:
        p1 = pipeline | "Create Socket" >> ronds.Socket("localhost", 9999)
        p2 = p1 | "Filter elements" >> ronds.Filter("value", "value is not null")
        p3 = p1 | "Filter elements 2" >> ronds.Filter("value", "value ='spark'")
        p2 | "console" >> ronds.Console('append')
        p3 | "console 2" >> ronds.Console('append')


def test_rule_cassandra_scan_console():
    options = PipelineOptions(
        transform_package='ronds_sdk.transforms.pandas.transforms',
        # enable_executor_debug=True,
        spark_repartition_num=1,
        process_data_window_duration=1,
        cassandra_start_datetime='2023-06-25 01:47:00',
        algorithm_path='AlgMock',
        algorithm_funcname='alg_mock.alg_mock'
    )
    with Pipeline(options=options) as p:
        p | "Rule Cassandra Scan" >> ronds.RulesCassandraScan([]) \
            | "algorithm" >> ronds.Algorithm() \
            | "Console" >> ronds.Console()


if __name__ == '__main__':
    # test_create()
    # test_socket()
    test_rule_cassandra_scan_console()
