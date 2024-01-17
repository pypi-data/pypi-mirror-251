import sys
from typing import Optional, TYPE_CHECKING, Set

import networkx as nx

from ronds_sdk.runners.planners import BFSPipeRule, PipeRule
from ronds_sdk.tools.constants import Parallel, ExpandChainType

if TYPE_CHECKING:
    from ronds_sdk import Pipeline, error
    from ronds_sdk.transforms.ptransform import PTransform
    from ronds_sdk.transforms.ray.base import RayTransform


__all__ = [
    'ParallelRule',
    'MergeSingleRule',
]


class ParallelRule(BFSPipeRule):

    def __init__(self):
        """
        Set parallel of every transform
            - if not set parallel, inherit from parent
            - if parent is root but not set parallel, set to 1 or node_nums
            - if more than one parent node, set to min parallel of parents
            - else, default parallel is 1
        """
        super().__init__()
        self._node_nums = None  # type: Optional[int]

    def with_node_nums(self, node_nums):
        self._node_nums = node_nums
        return self

    def node_nums(self):
        return self._node_nums or 1

    def on_match(self, transform, pipeline):
        # type: (PTransform, Pipeline) -> PTransform
        if transform.parallel is not None and transform.parallel > 0:
            return transform
        graph = pipeline.graph
        in_degree = graph.in_degree(transform)
        if in_degree == 0:
            return self._root_parallel(graph, transform)
        return self._node_parallel(graph, transform)

    def _root_parallel(self, graph, transform: 'RayTransform') -> 'RayTransform':
        successors = graph.successors(transform)
        if transform.parallel == Parallel.WORKER_NUM.value:
            transform.parallel = min(self.node_nums(), self.min_parallel(successors))
        return transform

    def _node_parallel(self, graph, transform: 'RayTransform') -> 'RayTransform':
        predecessors = graph.predecessors(transform)
        transform.parallel = self.min_parallel(predecessors)
        return transform

    @staticmethod
    def min_parallel(successors):
        parallel = None
        for transform in successors:
            if transform.parallel is None:
                continue
            parallel = min(parallel or sys.maxsize, transform.parallel)
        return parallel or 1


class MergeSingleRule(PipeRule):
    """
    Merge 1:1 sub graph, reduce IO between processes

       A
     /  \
     B   E
    |    |
    C    F

    transform to

      A
     /  \
   M1   M2

   M1 run task (B, C)
   M2 run task (E, F)
    """

    def apply(self, pipeline: 'Pipeline') -> 'Pipeline':
        new_graph = pipeline.graph.copy()
        from ronds_sdk.tools.networkx_util import NetworkUtil
        visited = set()
        for root_node in NetworkUtil.get_root_nodes(pipeline.graph):
            for node in NetworkUtil.bfs_nodes(root_node, pipeline.graph):
                self._apply(node, pipeline, new_graph, visited)
        pipeline.graph = new_graph
        return pipeline

    def _apply(self, node: 'RayTransform', pipeline: 'Pipeline', new_graph: 'nx.DiGraph', visited: Set):
        if node in visited:
            return
        visited.add(node)
        if not node.is_merge or node.expand_chain_type == ExpandChainType.ONE_TO_ALL:
            return

        # single child 1:1 sub graph, e.g. a:1 -> b:1 -> c:1
        sub_g = nx.DiGraph()
        depth, child = self._single_child(node, pipeline.graph, sub_g)
        if depth == 0:
            return
        if depth + 1 != sub_g.number_of_nodes():
            raise error.PlannerRuleError('depth error: %d != %d'
                                         % (depth + 1, sub_g.number_of_nodes()))

        for n in sub_g.nodes:
            visited.add(n)
        self._replace_stage(new_graph, sub_g, node, child)

    @staticmethod
    def _replace_stage(graph: 'nx.DiGraph', sub_g: 'nx.DiGraph', s_node, e_node):
        from ronds_sdk.transforms.ray.base import StageRayTransform
        stage_transform = StageRayTransform(sub_g)
        predecessors = list(graph.predecessors(s_node))
        successors = list(graph.successors(e_node))
        for u in sub_g.nodes:
            graph.remove_node(u)
        for predecessor in predecessors:
            graph.add_edge(predecessor, stage_transform)
        for successor in successors:
            graph.add_edge(stage_transform, successor)
        if stage_transform not in graph:
            graph.add_node(stage_transform)

    def _single_child(self, node: 'RayTransform', graph: 'nx.DiGraph', sub_g: 'nx.DiGraph'):
        depth = 0
        child = node
        if node is None:
            return depth, child

        successors = list(graph.successors(node))
        if len(successors) != 1:
            return depth, child

        successor = successors[0]  # type: 'RayTransform'
        if not successor.is_merge:
            return depth, child

        depth += 1
        sub_g.add_edge(node, successor)
        child_depth, child = self._single_child(successor, graph, sub_g)
        return depth + child_depth, child
