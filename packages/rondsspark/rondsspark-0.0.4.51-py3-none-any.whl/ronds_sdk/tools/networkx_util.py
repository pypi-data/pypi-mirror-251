from typing import List, TYPE_CHECKING, Any, Optional, Callable, Iterator

from networkx import DiGraph

if TYPE_CHECKING:
    from ronds_sdk.transforms.ptransform import PTransform


class NetworkUtil(object):

    @staticmethod
    def get_leaf_nodes(g):
        # type: (DiGraph) -> List[PTransform]
        for node in g.nodes():
            # noinspection PyCallingNonCallable
            if g.out_degree(node) == 0:
                yield node

    @staticmethod
    def get_root_nodes(g):
        # type: (DiGraph) -> List[PTransform]
        for node in g.nodes():
            # noinspection PyCallingNonCallable
            if g.in_degree(node) == 0:
                yield node

    @staticmethod
    def dfs_postorder_nodes(graph, root_node=None):
        # type: (DiGraph, Any) -> Iterator
        from networkx import depth_first_search
        if root_node is not None:
            for node in depth_first_search.dfs_postorder_nodes(graph, root_node):
                yield node
        else:
            for root_node in NetworkUtil.get_root_nodes(graph):
                for node in depth_first_search.dfs_postorder_nodes(graph, root_node):
                    yield node

    @staticmethod
    def bfs_nodes(root_node, graph, successor_match=None):
        # type: (Any, DiGraph, Optional[Callable[..., bool]]) -> Iterator
        from queue import Queue
        node_queue = Queue()
        node_queue.put(root_node)
        visited = set()
        while not node_queue.empty():
            node = node_queue.get()
            if node in visited:
                continue
            visited.add(node)
            yield node
            for successor in graph.successors(node):
                if successor_match is not None \
                        and not successor_match(successor):
                    continue
                node_queue.put(successor)
