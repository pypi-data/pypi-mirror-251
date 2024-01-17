"""
Hyper Graph
===========

A `hypergraph` originally means a graph containing `hyperedges`,
which is an edge connecting to more than 2 nodes.

That is just a special case of a more general form of hypergraph,
where an edge can connect (sub)graphs too.

Such a hypergraph is conceptually related to
- compositional graph
- hierarchical graph
- tree of graph 
- graph of graph
"""

from __future__ import annotations

from hashlib import sha256
from typing import Callable, Dict, Iterable, List, Set, Tuple, Type, Union

from gzeuge.graphs.schema import GraphProps, OrdinaryEdge
from networkx import MultiDiGraph


class HyperEdge:
    source: Union[str, Type['BaseHyperGraph']]
    target: Union[str, Type['BaseHyperGraph']]


class BaseHyperGraph:

    hash: str
    subgraphs: List[BaseHyperGraph]
    hyperedges: List[HyperEdge]
    const_foreign_key = 'foreign'
    const_root_key = '_root_'

    def __init__(self, hash: str, label: str):
        """
        Base class of hyper graph
        """
        self.hash = hash
        self.props = GraphProps(
            label=label
        )
        # ordinary graph
        self.graph = MultiDiGraph()
        self.add_node(hash=hash, **{BaseHyperGraph.const_root_key: True})

        # hyper (sub) graphs
        self.subgraphs = []
        # hyper edge among nodes/subgraphs
        self.hyperedges = []

    def add_node(self, hash: str, **attrs) -> BaseHyperGraph:
        self.graph.add_node(hash, **attrs)
        return self

    def add_subgraph(self, g: BaseHyperGraph) -> BaseHyperGraph:
        self.subgraphs.append(g)
        return self

    def add_nodes(self, nodes: List[Tuple[str, Dict]]) -> BaseHyperGraph:
        for hash, attrs in nodes:
            self.graph.add_node(hash, **attrs)
        return self

    def add_edge(self, edge: OrdinaryEdge) -> BaseHyperGraph:
        self.graph.add_edge(edge.source, edge.target, **edge.attributes)
        return self

    def add_edges(self, edges: List[OrdinaryEdge]) -> BaseHyperGraph:
        for edge in edges:
            self.add_edge(edge)
        return self

    def is_foreign_id(self, node: str):
        return node not in self.graph.nodes and node != self.hash

    def add_interedges(self, edges: List[OrdinaryEdge]) -> BaseHyperGraph:
        # edges interconnecting two different subgraphs
        for edge in edges:
            for hash in (edge.source, edge.target):
                if self.is_foreign_id(hash):
                    self.update_node_attrs(
                        hash,
                        **{BaseHyperGraph.const_foreign_key: True})
            self.graph.add_edge(edge.source, edge.target, **edge.attributes)
        return self

    def merge_interedges(self, edges: List[Tuple]) -> BaseHyperGraph:
        oedges = []
        for data in edges:
            attrs = dict() if len(data) == 2 else data[2]
            oedges.append(OrdinaryEdge(
                source=data[0], target=data[1], attributes=attrs))
        return self.add_interedges(oedges)

    def update_node_attrs(self, hash: str, **attrs):
        self.graph.add_node(hash, **attrs)

    def leaves(self) -> List[str]:
        """
        Get all nodes without outgoing edges
        """
        nodes = [node for node in self.graph.nodes
                 if self.graph.out_degree(node) == 0]
        return nodes

    def edgelist(self) -> List:
        for source, target, props in self.graph.edges(data=True):
            yield (source, target, props)

    def merge(
        self,
        elems: Union[Tuple[str, Dict], Tuple[str, str, Dict], BaseHyperGraph]
    ) -> BaseHyperGraph:
        for elem in elems:
            if isinstance(elem, BaseHyperGraph):
                self.add_subgraph(elem)
                continue
            if len(elem) == 2:
                if isinstance(elem[0], str) and isinstance(elem[1], dict):
                    self.add_node(hash=elem[0], **elem[1])
                else:
                    assert isinstance(elem[1], str)
                    self.add_edge(OrdinaryEdge(source=elem[0], target=elem[1]))
            elif len(elem) == 3:
                self.add_edge(OrdinaryEdge(source=elem[0],
                                           target=elem[1],
                                           attributes=elem[2]))
            else:
                raise ValueError(
                    f"Malformat, expected a tuple of 2 or 3, got {elem}")
        return self

    def __iadd__(
        self,
        elems: Union[Tuple[str, Dict], Tuple[str, str, Dict]]
    ) -> BaseHyperGraph:
        return self.merge(elems)

    @property
    def homenodes(self) -> List[str]:
        # Nodes excluding foreign nodes
        return [node for node in self.graph.nodes
                if not self.graph.nodes[node].get(BaseHyperGraph.const_foreign_key)
                and not self.graph.nodes[node].get(BaseHyperGraph.const_root_key)]

    @property
    def foreign_edges(self) -> List(OrdinaryEdge):
        nodes = set(self.homenodes)
        return [(s, t, data) for s, t, data in self.edgelist()
                if s not in nodes or t not in nodes]

    def edgeprops(self, source: str, target: str) -> Dict:
        return next(iter(self.graph.get_edge_data(source, target).values()), {})

    def print(
        self,
        indent=0,
        visited: Set = set([])
    ):
        if self.hash in visited:
            return
        visited.add(self.hash)
        _indent = '\t'*indent
        print(f"{_indent}{self.props.label}")
        own_nodes = set(self.homenodes)
        for node in self.homenodes:
            _content = self.graph.nodes[node]
            print(f"{_indent}{node} {_content}")
            for child in self.graph.successors(node):
                if child in own_nodes:
                    edgeprops = self.edgeprops(node, child)
                    print(f"{_indent}{node}->{child} {edgeprops}")
        for source, target, props in self.foreign_edges:
            print(f"{_indent}{source}->{target} {props}")
        for subg in self.subgraphs:
            subg.print(indent=indent+1, visited=visited)
