import os
import unittest

import ujson

import ronds_sdk as ronds
from ronds_sdk import Pipeline
from ronds_sdk.datasources.redis_manager import RedisManager
from ronds_sdk.options.pipeline_options import KafkaOptions, PipelineOptions
from ronds_sdk.parser.arg_parser import EditorArgParser
from ronds_sdk.parser.dag_parser import RuleBaseDagParser
from ronds_sdk.parser.rule_parser import EditorRuleParser
from ronds_sdk.runners.planners import OrderedPlanner
from ronds_sdk.runners.planners.core_rules import CoreRules
from ronds_sdk.tools import utils
from ronds_sdk.tools.constants import JsonKey
from ronds_sdk.tools.file_utils import FileUtils
from ronds_sdk.tools.utils import to_bool
from ronds_sdk.transforms.ray.streaming.algorithm import RuleWindowAlgorithm
from ronds_sdk.transforms.ray.streaming.filter import FilterByPhmRules
from ronds_sdk.transforms.ray.streaming.kafka import KafkaReader, KafkaAlgSender
from ronds_sdk.transforms.ray.streaming.shuffle import Shuffle


# noinspection SpellCheckingInspection
class PipelineTest(unittest.TestCase):
    arg_parser = EditorArgParser("arg.txt")
    rules = EditorRuleParser("point_config.json").load()
    kafka_topics = arg_parser.save_kafka_topics()
    reader_topics = arg_parser.kafka_reader_topic()['topics']
    alg_path = "D:/pythonProject/ruleEditor/ruleeditor"
    alg_func = "__init__.alg_call"
    reader_group_id = arg_parser.kafka_group_id()
    options = ronds.Options(
        enable_executor_debug=to_bool(os.getenv('EXECUTOR_DEBUG', False)),
        draw_pipeline=True,
        # algorithm
        algorithm_path=alg_path,
        algorithm_funcname=alg_func,
        algorithm_window_duration=arg_parser.window_duration(),
        algorithm_window_slide_duration=arg_parser.window_slide_window(),
        # kafka
        kafka_bootstrap_servers=arg_parser.kafka_bootstraps(),
        kafka_group_id=reader_group_id
    )

    def test_bind(self):
        p = Pipeline()
        p1 = p.bind(KafkaReader(self.reader_topics, self.options.view_as(KafkaOptions)),
                    p_value=None,
                    label="KafkaReader")
        p2 = p1 | "rule filter" >> FilterByPhmRules(self.rules)
        p3 = p1 | "kafka sender" >> KafkaAlgSender(self.kafka_topics, self.options)
        utils.draw_graph(p.graph)
        self.assertTrue(p1.pipeline == p)
        self.assertTrue(p2.pipeline == p)
        self.assertTrue(p3.pipeline == p)

    def test_graph(self):
        from ronds_sdk.runners.ray_runner import RayStreamRunner
        p = Pipeline(options=self.options, runner=RayStreamRunner)
        p | 'KafkaReaders' >> KafkaReader(self.reader_topics, self.options.view_as(KafkaOptions)) \
            | "rule filter" >> FilterByPhmRules(self.rules) \
            | "Shuffle" >> Shuffle(JsonKey.RULE_GROUP.value) \
            | "algorithm" >> RuleWindowAlgorithm(self.rules, 'Time', self.options) \
            | "kafka sender" >> KafkaAlgSender(self.kafka_topics, self.options)

        p = OrderedPlanner([
            CoreRules.PARALLEL_RULE.with_node_nums(1),
            CoreRules.RAY_STREAM_CONVERT_RULE,
        ]).find_best(p)
        utils.draw_graph(p.graph)
        print(utils.uid())
        self.assertTrue(True)

    def test_ray_planner(self):
        pipeline = RuleBaseDagParser("arg.txt",
                                     "D:/pythonProject").pipeline()
        pipeline.run().wait_until_finish()
        self.assertTrue(True)

    def test_redis_get(self):
        redis_manager = RedisManager(PipelineOptions(
            redis_host="172.16.0.112",
            redis_port=7000,
            redis_password="redis123",
            redis_username="default",
        ))
        print(redis_manager.set('key2', "1111", 10))
        print(redis_manager.get('key2'))
        self.assertTrue(True)

    def test_alg(self):

        try:
            if True:
                i = 3
        except Exception as ex:
            raise ex

        print(i)
        self.assertTrue(True)

    def test_alg_editor(self):
        from ronds_sdk.transforms.pandas.transforms import Algorithm
        alg_record = FileUtils.load_json('test_data.json')
        alg = Algorithm(ronds.Algorithm("D:/pythonProject/ruleEditor/ruleeditor",
                                        "__init__.alg_call"),
                        self.options)
        row = alg.algorithm_call(alg_record)
        print(row)
        strs = '{"id":"3a0b5da3-66be-a3f5-62bc-9ed74d0a6d43","Value":89,"Time":"2023-10-16 15:39:05","Properties":{}}'
        d = ujson.loads(strs)
        print(ujson.dumps(d))
        print(float(18))

        self.assertTrue(True)

    def test_phm_rule_base_ray(self):
        from ronds_sdk.templates import phm_rule_base_ray
        phm_rule_base_ray.run(None,
                              "D:/pythonProject/rulebase",
                              "__init__.alg_call",
                              "rule_base_arg.txt",
                              parallel=2)
        self.assertTrue(True)
