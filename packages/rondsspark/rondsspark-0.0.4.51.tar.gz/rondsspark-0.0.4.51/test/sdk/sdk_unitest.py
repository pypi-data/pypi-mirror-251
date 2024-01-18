import datetime
import sys
import unittest
from datetime import date
from typing import Callable

import pandas as pd
from pyspark.sql import SparkSession

import ronds_sdk.transforms.pandas.transforms as py_df
from ronds_sdk.datasources.cassandra_manager import ProcessDataManager
from ronds_sdk.options.pipeline_options import PipelineOptions, SparkRunnerOptions, CassandraOptions
from ronds_sdk.tools import utils
from ronds_sdk.tools.utils import RuleParser, GraphParser
from ronds_sdk.transforms import ronds


def mock_data():
    return [(1, 1., 'string1', date(2000, 1, 1), datetime.datetime(2000, 1, 1, 12, 0)),
            (2, 2., 'string2', date(2000, 2, 1), datetime.datetime(2000, 1, 2, 12, 0)),
            (3, 3., 'string3', date(2000, 3, 1), datetime.datetime(2000, 1, 3, 12, 0))]


class SdkUnitTest(unittest.TestCase):

    def test_rules_load(self):
        rule_parser = RuleParser('./rule_config.json')
        rules = rule_parser.load()
        self.assertTrue(isinstance(rules, list))
        self.assertTrue(len(rules) > 0)

    def test_spark_json_load(self):
        spark = SparkSession.builder.getOrCreate()
        rules_parser = RuleParser("rule_config.json")
        df = spark.createDataFrame(rules_parser.load())
        print(df.schema)
        rules = df.collect()
        print(rules)
        self.assertTrue(len(rules) > 1)

    def test_spark_runner_options(self):
        options = PipelineOptions(
            spark_repartition_num=3
        )
        num = options.view_as(SparkRunnerOptions).spark_repartition_num
        print('num: %d' % num)
        self.assertTrue(num == 3)

    def test_list_str(self):
        data = [
            {'a': 1, 'b': [[2, 3]], 'c': [{'d': 1}, 3]},
            {'a': 2, 'b': [[3]], 'c': [{'d': 1}, 3]},
            {'a': 3, 'b': [[4]], 'c': [{'d': 1}, 3]},
        ]
        dt = pd.DataFrame(data)
        self.assertTrue(dt['c'][0][0]['d'] == 1)
        dt_dict = dt.to_dict('records')
        self.assertTrue(id(dt['c'][0]) == id(dt_dict[0]['c']))
        print("records json: %s" % dt_dict)
        print("dict json: %s" % dt.to_dict())
        print("index json: %s" % dt.to_dict('index'))
        print("*" * 20)
        for i, row in dt.iterrows():
            print("%s: table json: %s" % (i, row.to_json(orient='table')))
            print("%s: records json: %s" % (i, row.to_json(orient='records')))
            print("%s: split json: %s" % (i, row.to_json(orient='split')))
            print("%s: index json: %s" % (i, row.to_json(orient='index')))

    def test_list_tuple(self):
        rows = [('key1', 'v1'), ('key2', 'v2')]
        for key, value in rows:
            print(key, value)
        self.assertTrue(True)

    def test_algorithm(self):
        options = PipelineOptions(
            algorithm_path='AlgMock',
            algorithm_funcname='alg_mock.alg_mock'
        )
        alg = py_df.Algorithm(ronds.Algorithm(), options)
        func = alg.algorithm_func
        self.assertTrue(isinstance(func, Callable))
        result = func("test data")
        self.assertTrue('test data' == result)

    def test_to_bool(self):
        self.assertTrue(utils.to_bool(None) is False)
        self.assertTrue(utils.to_bool('') is False)
        self.assertTrue(utils.to_bool('Fa') is False)
        self.assertTrue(utils.to_bool('False') is False)
        self.assertTrue(utils.to_bool('true') is True)
        self.assertTrue(utils.to_bool(True) is True)
        self.assertTrue(utils.to_bool(False) is False)

    # noinspection SpellCheckingInspection
    def test_import(self):
        import importlib.machinery
        model_path = '__init__'
        alg_absolute_path = 'D:/pythonProject/ruleEditor/ruleeditor/'
        sys.path.append(alg_absolute_path)
        loader = importlib.machinery.SourceFileLoader(model_path, alg_absolute_path + '/__init__.py')
        alg_model = loader.load_module(model_path)
        alg_call = getattr(alg_model, 'alg_call')
        self.assertTrue(isinstance(alg_call, Callable))

    # noinspection SpellCheckingInspection
    def test_import2(self):
        import importlib.util
        model_path = '__init__'
        alg_absolute_path = 'D:/pythonProject/ruleEditor/ruleeditor/'
        sys.path.append(alg_absolute_path)
        spec = importlib.util.spec_from_file_location(model_path, alg_absolute_path + '/__init__.py')
        alg_model = importlib.util.module_from_spec(spec)
        alg_call = getattr(alg_model, 'alg_call')
        self.assertTrue(isinstance(alg_call, Callable))

    def test_cassandra_scan(self):
        options = CassandraOptions(
            process_data_window_duration=30000,
        )
        process_manager = ProcessDataManager(options)
        uid_list = ['3a0b5da3-66be-a3f5-62bc-9ed74d0a6d43']
        end_datetime = datetime.datetime.now()
        delta = datetime.timedelta(seconds=options.process_data_window_duration)
        start_datetime = end_datetime - delta
        result = process_manager.window_select(uid_list, start_datetime, end_datetime)
        for row in result:
            print(row)
        self.assertTrue(True)

    def test_kafka_send(self):
        json_parser = RuleParser("D:/documents/PHM/test.json")
        rule_parser = GraphParser("D:/documents/PHM/test.json")
        json_dict = json_parser.load()
        df = pd.DataFrame(json_dict)
        from ronds_sdk import SendAlgJsonKafka
        sender = py_df.SendAlgJsonKafka(SendAlgJsonKafka(rule_parser.kafka_source_topics()),
                                        options=PipelineOptions(kafka_send_mock=True)
                                        )
        sender.send_exception(df, "alarm_event_json")
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
