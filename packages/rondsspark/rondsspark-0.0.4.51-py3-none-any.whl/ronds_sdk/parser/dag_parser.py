import os
from typing import TYPE_CHECKING, Dict, Callable

import networkx as nx

from ronds_sdk import Pipeline, error
from ronds_sdk.options.pipeline_options import AlgorithmOptions
from ronds_sdk.options.pipeline_options import HttpOptions, PipelineOptions
from ronds_sdk.parser import Activity
from ronds_sdk.parser.arg_parser import ArgParser
from ronds_sdk.tools import utils
from ronds_sdk.tools.constants import JsonKey, Default
from ronds_sdk.transforms.ray.base import RayTransform
from ronds_sdk.transforms.ray.streaming.transform import GraphTransform

if TYPE_CHECKING:
    from ronds_sdk.transforms.ray.base import RayTransform


class RuleBaseDagParser(object):

    def __init__(self, file_path: str = None, base_dir: str = None):
        """
        rule base dag parser, convert rule base dag to pipeline
        :param file_path: graph file (arg.txt) path
        :param base_dir: worker flow base dir that contains arg.txt, algorithms python.
        """
        self._arg_path = file_path
        self._arg_parser = ArgParser(file_path)
        self._base_dir = base_dir or os.path.dirname(file_path)

    @property
    def arg_parser(self):
        return self._arg_parser

    def pipeline(self) -> Pipeline:
        dag = self.dag()
        if self._is_rule_editor(dag):
            return self._rule_editor_pipeline(self._arg_path)
        return self._rule_base_pipeline(dag)

    def _rule_base_pipeline(self, dag: nx.DiGraph) -> pipeline:
        """
        convert rule base dag to pipeline
        :param dag: rule base dag
        :return:
        """
        from ronds_sdk.runners.ray_runner import RayStreamRunner
        from ronds_sdk.tools.networkx_util import NetworkUtil
        options = PipelineOptions(
            ray_merge=self._arg_parser.calc_config_is_merge()
        )
        worker_flow_id = self._arg_parser.get_worker_flow_id
        factory = RuleBaseRayTransformFactory(worker_flow_id, self._base_dir, self._arg_parser)
        visited = dict()
        p = Pipeline(namespace=worker_flow_id, options=options, runner=RayStreamRunner)
        for root_node in NetworkUtil.get_root_nodes(dag):
            for node in NetworkUtil.bfs_nodes(root_node, dag):
                s_pt = visited.setdefault(node, factory.create(node))
                successors = list(dag.successors(node))
                if utils.collection_empty(successors):
                    if s_pt not in p.nodes():
                        p.add_node(s_pt)
                    continue
                for t_node in successors:
                    t_pt = visited.setdefault(t_node, factory.create(t_node))
                    p.add_edge(s_pt, t_pt)

        return p

    @staticmethod
    def _is_rule_editor(graph: nx.DiGraph) -> bool:
        """
        check if graph is rule editor.
        True: only containing one activity - 'RuleEditorRayActivity'
        :param graph: rule editor graph
        :return: True or False
        """
        if len(graph.nodes()) == 1:
            node = list(graph.nodes())[0]  # type: Activity
            return node.actName == JsonKey.RULE_EDITOR_ACTIVITY.v
        return False

    def _rule_editor_pipeline(self, graph_path: str) -> Pipeline:
        """
        convert rule editor graph to pipeline
        :param graph_path: rule editor graph path (arg.txt file path)
        :return: rule editor pipeline
        """
        from ronds_sdk.templates import phm_rules_editor_ray

        base_dir = self._base_dir
        alg_path = f"{base_dir}/{Default.RULE_EDITOR_ALG_PATH.v}"
        rule_path = f"{alg_path}/{Default.RULE_EDITOR_RULE_PATH.v}"
        alg_func = Default.RULE_EDITOR_ALG_FUNC.v
        return phm_rules_editor_ray.pipeline(rule_path, alg_path, alg_func, graph_path)

    def dag(self) -> nx.DiGraph:
        """
        load rule base dag from arg.txt
        :return: rule base dag
        """
        graph = nx.DiGraph()
        activities = self.arg_parser.get_activities()
        act_map = {activity.aid: activity for activity in activities}
        diagram = self.arg_parser.get_diagram()
        if utils.collection_empty(diagram.get('edges')) and len(diagram.get('nodes')) == 1:
            source = act_map[diagram['nodes'][0]['id']]
            graph.add_node(source)
        else:
            for edge in diagram['edges']:
                source_id = edge['source']
                target_id = edge['target']
                if source_id not in act_map or target_id not in act_map:
                    raise error.ParserError(
                        f'diagram invalid activity id: [{source_id}, {target_id}]')
                source = act_map[source_id]
                target = act_map[target_id]
                graph.add_edge(source, target)
        return graph


class RuleBaseRayTransformFactory(object):

    def __init__(self,
                 worker_flow_id: str,
                 base_dir: str,
                 arg_parser: 'ArgParser',
                 ):
        """
        ray transform factory from arg.txt config
        :param worker_flow_id: worker flow id
        :param base_dir: base dir for arg.txt or algorithm python directory
        :param arg_parser: arg_parser
        """
        self.worker_flow_id = worker_flow_id
        self.base_dir = base_dir
        num_cpus, num_gpus, parallel, is_merge = arg_parser.get_calc_config()
        self.num_cpus = num_cpus
        self.num_gpus = num_gpus
        self.parallel = parallel
        self.global_is_merge = is_merge
        self.creator = self._default_create()
        # Create a ComponentIdMap for assigning IDs to components.
        from ronds_sdk.pipeline import ComponentIdMap
        self.component_id_map = ComponentIdMap()

    def _default_create(self) -> Dict[str, Callable[['Activity'], 'RayTransform']]:
        return {
            'KafkaReader': self.kafka_reader,
            'RuleBaseAlgorithm': self.rule_base_algorithm,
            'RuleBaseAlgorithmWithBuffer': self.rule_base_algorithm_with_buffer,
            'RuleSaveRedisBuffer': self.rule_save_redis_buffer,
            'RuleReadRedisBuffer': self.rule_read_redis_buffer,
            'KafkaAlgSender': self.kafka_alg_sender,
            'HttpGetDevModel': self.read_http_device_model,
            'RedisReadDevModel': self.rule_redis_dev_model,
            'RedisReadDevModelAndDynaPara': self.redis_read_dev_model_and_dyna_para,
            'RedisUpdateDynaPara': self.rule_update_dyna_para,
            'KafkaSender': self.kafka_sender,
            'Shuffle': self.shuffle,
            'TrendProcessIndexHandle': self.trend_process_index_handle,
            'TrendTsDatasIndexHandle': self.trend_ts_datas_index_handle,
            'TrendFeatureDatasIndexHandle': self.trend_feature_datas_index_handle,
            'TrendTraitDatasIndexHandle': self.trend_trait_datas_index_handle,
            'TransformSecondAlarmConfirm': self.graph_transform,
            'ESSaveAlgException': self.es_save_alg_exception
        }

    def create(self, activity: Activity) -> 'RayTransform':
        """
        create ray transform
        :param activity: config
        :return: RayTransform instance
        """
        if activity.actName not in self.creator:
            raise error.ParserError('invalid activity: [%s]' % activity)
        pt = self.creator[activity.actName](activity)  # type: 'RayTransform'
        if pt is None:
            raise error.ParserError('invalid activity: [%s]' % activity)
        return self.component_id_map.auto_label(pt)

    def _resources(self, activity: Activity):
        """
        task resources costs from activity or default config: num_cpus, num_gpus, parallel
        :param activity: config of activity
        :return: num_cpus, num_gpus, parallel
        """
        num_cpus = activity.num_cpus() or self.num_cpus
        num_gpus = activity.num_gpus() or self.num_gpus
        parallel = activity.parallel() or self.parallel
        return num_cpus, num_gpus, parallel

    def _is_merge(self, activity: Activity):
        return self.global_is_merge and activity.is_merge()

    def kafka_reader(self, activity: Activity) -> 'RayTransform':
        """
        KafkaReader factory
        :param activity: config
        :return: KafkaReader instance
        """
        from ronds_sdk.transforms.ray.streaming.kafka import KafkaReader
        from ronds_sdk.options.pipeline_options import KafkaOptions

        kafka_source = activity.act_config['kafkaSource']  # type: Dict
        topics = kafka_source['topics']
        kafka_port = kafka_source['port']
        kafka_servers = ['%s:%s' % (s, kafka_port) for s in kafka_source['bootstraps'].split(',')]
        num_cpus, num_gpus, parallel = self._resources(activity)
        group_id = activity.act_config['groupId'] \
            if 'groupId' in activity.act_config and utils.is_not_blank(activity.act_config['groupId']) \
            else self.worker_flow_id
        options = KafkaOptions(
            pipeline_namespace=self.worker_flow_id,
            kafka_bootstrap_servers=','.join(kafka_servers),
            kafka_group_id=group_id,
            kafka_auto_offset_reset=activity.act_config.get('autoOffsetReset', 'largest'),
        )
        schema = (
            (JsonKey.ID.value, str),
            (JsonKey.MESSAGE.value, dict),
            (JsonKey.TOPIC.value, str),
            (JsonKey.ARRIVE_TIME.value, int),
            (JsonKey.PARTITION.value, int),
            (JsonKey.OFFSET.value, int),
        )
        return KafkaReader(topics, options,
                           parallel=parallel, num_cpus=num_cpus, num_gpus=num_gpus, schema=schema)

    def rule_base_algorithm(self, activity: Activity) -> 'RayTransform':
        """
        RuleBaseAlgorithm factory
        :param activity: config
        :return: RuleBaseAlgorithm instance
        """
        from ronds_sdk.transforms.ray.streaming.algorithm import RuleBaseAlgorithm
        options = _get_algorithm_options(activity.act_config[JsonKey.RONDS_API.v],
                                         worker_flow_id=self.worker_flow_id, base_dir=self.base_dir)
        graph_config = self.get_graph_config(activity)
        num_cpus, num_gpus, parallel = self._resources(activity)
        is_merge = self._is_merge(activity)
        return RuleBaseAlgorithm(graph_config, options,
                                 parallel=parallel, num_cpus=num_cpus, num_gpus=num_gpus, is_merge=is_merge)

    def rule_base_algorithm_with_buffer(self, activity: Activity) -> 'RayTransform':
        """
        RuleBaseAlgorithmWithBuffer factory
        :param activity: config
        :return: RuleBaseAlgorithmWithBuffer instance
        """
        from ronds_sdk.transforms.ray.streaming.algorithm import RuleBaseAlgorithmWithBuffer
        graph_config = self.get_graph_config(activity)
        num_cpus, num_gpus, parallel = self._resources(activity)
        buffer_sources = {k: v for k, v in activity.act_config.items() if k.endswith('Buffer')}

        algorithm_options = _get_algorithm_options(activity.act_config[JsonKey.RONDS_API.v],
                                                   worker_flow_id=self.worker_flow_id, base_dir=self.base_dir)
        read_rule_algorithm_buffer = activity.act_config[JsonKey.READ_RULE_ALGORITHM_BUFFER.v]
        read_redis_source = read_rule_algorithm_buffer['redisSource']
        read_cassandra_source = read_rule_algorithm_buffer['cassandraSource']
        is_merge = self._is_merge(activity)
        if read_cassandra_source is not None:
            redis_options = _get_redis_options(read_redis_source)
            cassandra_options = _get_cassandra_options(read_cassandra_source)
            return RuleBaseAlgorithmWithBuffer(graph_config, buffer_sources,
                                               algorithm_options + redis_options + cassandra_options,
                                               parallel=parallel, num_cpus=num_cpus,
                                               num_gpus=num_gpus, is_merge=is_merge)
        else:
            redis_options = _get_redis_options(read_redis_source)
            return RuleBaseAlgorithmWithBuffer(graph_config, buffer_sources,
                                               algorithm_options + redis_options, parallel=parallel,
                                               num_cpus=num_cpus, num_gpus=num_gpus, is_merge=is_merge)

    # noinspection SpellCheckingInspection
    @staticmethod
    def get_graph_config(activity: Activity) -> str:
        ronds_ai = activity.act_config[JsonKey.RONDS_API.v]  # type: dict
        execute_script = ronds_ai[JsonKey.EXECUTE_SCRIPT.v].split('/')
        if len(execute_script) != 2:
            raise error.ParserError('invalid activity executeScript config: [%s]' % activity)
        graph_config = ronds_ai.get(JsonKey.GRAPH_CONFIG.v)
        return graph_config

    def rule_save_redis_buffer(self, activity: Activity) -> 'RayTransform':
        from ronds_sdk.transforms.ray.streaming.redis import RuleSaveRedisBuffer
        num_cpus, num_gpus, parallel = self._resources(activity)
        return RuleSaveRedisBuffer(self.worker_flow_id,
                                   _get_redis_options(activity.act_config['redisSource'],
                                                      activity.act_config['saveTime']),
                                   parallel=parallel, num_cpus=num_cpus, num_gpus=num_gpus)

    def rule_update_dyna_para(self, activity: Activity) -> 'RayTransform':
        from ronds_sdk.transforms.ray.streaming.redis import RedisUpdateDynaPara
        num_cpus, num_gpus, parallel = self._resources(activity)
        return RedisUpdateDynaPara(_get_redis_options(activity.act_config['redisSource']),
                                   parallel=parallel, num_cpus=num_cpus, num_gpus=num_gpus)

    def rule_read_redis_buffer(self, activity: Activity) -> 'RayTransform':
        from ronds_sdk.transforms.ray.streaming.redis import RuleReadRedisBuffer
        num_cpus, num_gpus, parallel = self._resources(activity)
        return RuleReadRedisBuffer(self.worker_flow_id, _get_redis_options(activity.act_config['redisSource']),
                                   parallel=parallel, num_cpus=num_cpus, num_gpus=num_gpus)

    def rule_redis_dev_model(self, activity: Activity) -> 'RayTransform':
        from ronds_sdk.transforms.ray.streaming.redis import RedisReadDevModel
        num_cpus, num_gpus, parallel = self._resources(activity)
        return RedisReadDevModel(_get_redis_options(activity.act_config['redisSource']),
                                 parallel=parallel, num_cpus=num_cpus, num_gpus=num_gpus)

    def redis_read_dev_model_and_dyna_para(self, activity: Activity) -> 'RayTransform':
        from ronds_sdk.transforms.ray.streaming.redis import RedisReadDevModelAndDynaPara
        num_cpus, num_gpus, parallel = self._resources(activity)
        return RedisReadDevModelAndDynaPara(_get_redis_options(activity.act_config['redisSource']),
                                            parallel=parallel, num_cpus=num_cpus, num_gpus=num_gpus)

    def read_http_device_model(self, activity: Activity) -> 'RayTransform':
        from ronds_sdk.transforms.ray.streaming.http import HttpGetDevModel
        num_cpus, num_gpus, parallel = self._resources(activity)
        http_source = activity.act_config['httpSource']
        options = HttpOptions(
            pipeline_namespace=self.worker_flow_id,
            http_port=http_source['port'],
            route=http_source['route'],
            address=http_source['address'],
            agreement=http_source['agreement'],
            path=http_source['path'],
            mode=http_source['mode']
        )

        return HttpGetDevModel(options, parallel=parallel, num_cpus=num_cpus, num_gpus=num_gpus)

    def kafka_alg_sender(self, activity: Activity) -> 'RayTransform':
        """
        KafkaAlgSender factory
        :param activity: config
        :return: KafkaAlgSender instance
        """
        from ronds_sdk.transforms.ray.streaming.kafka import KafkaAlgSender
        from ronds_sdk import PipelineOptions

        num_cpus, num_gpus, parallel = self._resources(activity)
        kafka_sources = {k: v for k, v in activity.act_config.items() if k.endswith('KafkaSource')}
        options = PipelineOptions(
            pipeline_namespace=self.worker_flow_id,
        )
        return KafkaAlgSender(kafka_sources, options,
                              parallel=parallel, num_cpus=num_cpus, num_gpus=num_gpus)

    # noinspection SpellCheckingInspection
    def shuffle(self, activity: Activity) -> 'RayTransform':
        """
        Shuffle factory
        :param activity: config
        :return: Shuffle instance
        """
        from ronds_sdk.transforms.ray.streaming.shuffle import Shuffle
        import importlib

        num_cpus, num_gpus, parallel = self._resources(activity)
        shuffle_key = activity.act_config['shuffleKey']
        partitioner = activity.act_config['partitioner']
        module_name = "ronds_sdk.tools.shuffle"
        module = importlib.import_module(module_name)
        partitioner_func = getattr(module, partitioner)
        return Shuffle(shuffle_key, partitioner_func, parallel=parallel, num_cpus=num_cpus, num_gpus=num_gpus)

    def kafka_sender(self, activity: Activity) -> 'RayTransform':
        """
        KafkaSender factory
        :param activity: config
        :return: KafkaSender instance
        """
        from ronds_sdk.transforms.ray.streaming.kafka import KafkaSender
        from ronds_sdk import PipelineOptions
        num_cpus, num_gpus, parallel = self._resources(activity)
        kafka_source = activity.act_config['kafkaSource']  # type: Dict
        options = PipelineOptions(
            pipeline_namespace=self.worker_flow_id,
        )
        return KafkaSender(kafka_source, options,
                           parallel=parallel, num_cpus=num_cpus, num_gpus=num_gpus)

    def trend_process_index_handle(self, activity: Activity) -> 'RayTransform':
        """
        TrendProcessIndexHandle factory
        :param activity: config
        :return: TrendProcessIndexHandle instance
        """
        from ronds_sdk.transforms.ray.streaming.trend_transform import TrendProcessIndexHandle
        minio_options, num_cpus, num_gpus, parallel = self._set_trend_params(activity)
        return TrendProcessIndexHandle(minio_options,
                                       parallel=parallel, num_cpus=num_cpus, num_gpus=num_gpus)

    def trend_ts_datas_index_handle(self, activity: Activity) -> 'RayTransform':
        """
        TrendTsDatasIndexHandle factory
        :param activity: config
        :return: TrendTsDatasIndexHandle instance
        """
        from ronds_sdk.transforms.ray.streaming.trend_transform import TrendTsDatasIndexHandle
        minio_options, num_cpus, num_gpus, parallel = self._set_trend_params(activity)
        return TrendTsDatasIndexHandle(minio_options,
                                       parallel=parallel, num_cpus=num_cpus, num_gpus=num_gpus)

    def trend_feature_datas_index_handle(self, activity: Activity) -> 'RayTransform':
        """
        TrendFeatureDatasIndexHandle factory
        :param activity: config
        :return: TrendFeatureDatasIndexHandle instance
        """
        from ronds_sdk.transforms.ray.streaming.trend_transform import TrendFeatureDatasIndexHandle
        minio_options, num_cpus, num_gpus, parallel = self._set_trend_params(activity)
        return TrendFeatureDatasIndexHandle(minio_options,
                                            parallel=parallel, num_cpus=num_cpus, num_gpus=num_gpus)

    def trend_trait_datas_index_handle(self, activity: Activity) -> 'RayTransform':
        """
        TrendTraitDatasIndexHandle factory
        :param activity: config
        :return: TrendTraitDatasIndexHandle instance
        """
        from ronds_sdk.transforms.ray.streaming.trend_transform import TrendTraitDatasIndexHandle
        minio_options, num_cpus, num_gpus, parallel = self._set_trend_params(activity)
        return TrendTraitDatasIndexHandle(minio_options,
                                          parallel=parallel, num_cpus=num_cpus, num_gpus=num_gpus)

    def graph_transform(self, activity: Activity) -> 'RayTransform':
        """
        GraphTransform factory
        :param activity: config
        :return: GraphTransform instance
        """
        num_cpus, num_gpus, parallel = self._resources(activity)
        return GraphTransform(parallel=parallel, num_cpus=num_cpus, num_gpus=num_gpus)

    # noinspection SpellCheckingInspection
    def es_save_alg_exception(self, activity: Activity) -> 'RayTransform':
        """
        ESSaveAlgException factory
        :param activity: config
        :return: ESSaveAlgException instance
        """
        from ronds_sdk.transforms.ray.streaming.elasticsearch import ESSaveAlgException
        from ronds_sdk.options.pipeline_options import ESOptions
        num_cpus, num_gpus, parallel = self._resources(activity)
        es_source = activity.act_config['elasticsearchSource']  # type: Dict
        # 定义索引设置
        settings = _get_es_setting()
        es_options = ESOptions(
            pipeline_namespace=self.worker_flow_id,
            nodes=[node for node in es_source['nodes'].split(',')],
            port=es_source['port'],
            index=es_source['index'],
            index_auto_create=True if es_source['indexautocreate'] == 'true' else False,
            mapping=settings
        )
        return ESSaveAlgException(es_options,
                                  parallel=parallel, num_cpus=num_cpus, num_gpus=num_gpus)

    def _set_trend_params(self, activity):
        from ronds_sdk.options.pipeline_options import MinioOptions
        num_cpus, num_gpus, parallel = self._resources(activity)
        minio_source = activity.act_config['minioSource']  # type: Dict
        minio_options = MinioOptions(
            pipeline_namespace=self.worker_flow_id,
            address=minio_source['address'],
            port=minio_source['port'],
            username=minio_source['username'],
            password=minio_source['password'],
            buckets=minio_source['buckets'],
        )
        return minio_options, num_cpus, num_gpus, parallel


def _get_redis_options(redis_source: dict, expire_time=None):
    from ronds_sdk.options.pipeline_options import RedisOptions
    redis_nodes = []
    for item in redis_source['address'].split(','):
        node = item.split(":")
        redis_nodes.append({'host': node[0], 'port': node[1]})
    return RedisOptions(redis_nodes=redis_nodes,
                        redis_username=redis_source.get('username'),
                        redis_password=redis_source.get('password'),
                        redis_expire_time=int(expire_time or '7') * 24 * 60 * 60)


# noinspection SpellCheckingInspection
def _get_algorithm_options(ronds_ai: Dict, worker_flow_id: str, base_dir: str) -> AlgorithmOptions:
    from ronds_sdk.options.pipeline_options import AlgorithmOptions
    execute_script = ronds_ai[JsonKey.EXECUTE_SCRIPT.v].split('/')
    if len(execute_script) != 2:
        raise error.ParserError('invalid ronds_ai executeScript config: [%s]' % ronds_ai)
    main_file = os.path.splitext(execute_script[1])[0]
    return AlgorithmOptions(pipeline_namespace=worker_flow_id,
                            algorithm_path='%s/%s.zip' % (base_dir, execute_script[0]),
                            algorithm_funcname="%s.%s" % (main_file, Default.RULE_BASE_ALG_FUNC.v))


def _get_cassandra_options(cassandra_source: Dict):
    from ronds_sdk.options.pipeline_options import CassandraOptions
    # noinspection SpellCheckingInspection
    return CassandraOptions(cassandra_host=cassandra_source['address'].split(','),
                            cassandra_keyspace=cassandra_source["keyspace"],
                            cassandra_table_process=cassandra_source["dtnames"][0])


# noinspection SpellCheckingInspection
def _get_es_setting():
    settings = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "category": {
                    "type": "keyword"
                },
                "create_time": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss||epoch_millis||date_optional_time"
                              "||yyyy-MM-dd HH:mm:ss.S||yyyy-MM-dd HH:mm:ss.SS||yyyy-MM-dd HH:mm:ss.SSS"
                              "||yyyy-MM-dd HH:mm:ss.SSSS||yyyy-MM-dd HH:mm:ss.SSSSS"
                              "||yyyy-MM-dd HH:mm:ss.SSSSSS"
                },
                "creator": {
                    "type": "keyword"
                },
                "exception_type": {
                    "type": "keyword"
                },
                "group": {
                    "type": "keyword"
                },
                "message": {
                    "type": "text",
                    "index": False
                },
                "record_id": {
                    "type": "keyword"
                },
                "source": {
                    "type": "text",
                    "index": False
                },
                "stack": {
                    "type": "text",
                    "index": False
                },
                "total": {
                    "type": "integer"
                },
                "workflowid": {
                    "type": "keyword"
                }
            }
        }
    }
    return settings
