from queue import Queue
from typing import TYPE_CHECKING, List

import networkx as nx
from networkx import Graph

from ronds_sdk import logger_config
from ronds_sdk.tools import utils

if TYPE_CHECKING:
    from ronds_sdk.transforms.ptransform import PTransform
    from ronds_sdk import Pipeline, error, logger_config


logger = logger_config.config()


class PipeRule(object):
    """
    random traversal for graph nodes
    """

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def match(self, transform: 'PTransform', pipeline: 'Pipeline') -> bool:
        return True

    def on_match(self, transform: 'PTransform', pipeline: 'Pipeline') -> 'PTransform':
        return transform

    def apply(self, pipeline: 'Pipeline') -> 'Pipeline':
        new_graph = pipeline.graph.copy()
        for node in pipeline.nodes():
            if self.match(node, pipeline):
                new_node = self.on_match(node, pipeline)
                if new_node != node:
                    nx.relabel_nodes(new_graph, {node: new_node}, copy=False)
        pipeline.graph = new_graph
        return pipeline


class ExpandedPipeRule(PipeRule):
    """
    pipeline has been expanded, call RayStreamConvertRule in advance
    """

    def apply(self, pipeline: 'Pipeline') -> 'Pipeline':
        if not pipeline.expand:
            raise error.PlannerError('pipeline not expand, call RayStreamConvertRule in advance')
        return super().apply(pipeline)


class BFSPipeRule(PipeRule):
    """
    BFS traversal for graph nodes
    """

    def apply(self, pipeline: 'Pipeline') -> 'Pipeline':
        visited = set()
        new_graph = pipeline.graph.copy()
        from ronds_sdk.tools.networkx_util import NetworkUtil
        for root_node in NetworkUtil.get_root_nodes(pipeline.graph):
            self._root_apply(root_node, pipeline, new_graph, visited)
        pipeline.graph = new_graph
        return pipeline

    def _root_apply(self, root_node, pipeline, new_graph, visited):
        # type: ('BFSPipeRule', PTransform, Pipeline, Graph, set) -> None
        node_queue = Queue()
        node_queue.put(root_node)
        while not node_queue.empty():
            node = node_queue.get()
            if node in visited:
                continue
            visited.add(node)
            if not self.match(node, pipeline):
                continue
            new_node = self.on_match(node, pipeline)
            if new_node != node:
                nx.relabel_nodes(new_graph, {node: new_node}, copy=False)
            successors = pipeline.successors(node)
            for successor in successors:
                node_queue.put(successor)


class OrderedPlanner(object):

    def __init__(self, rules: List['PipeRule'] = ()):
        self.rules = rules

    def find_best(self, pipeline: 'Pipeline') -> 'Pipeline':
        if utils.collection_empty(self.rules):
            return pipeline
        for rule in self.rules:
            pipeline = rule.apply(pipeline)
            logger.info('rule: %s applied successfully' % rule)
        return pipeline
