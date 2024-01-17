"""
Graph Basics
============

Tree
- add_edge
- add_edges
- append_leaf
- height

Terms
-----

- open leaves: ...
"""

from __future__ import annotations

import re
from collections import defaultdict
from hashlib import sha256
from typing import Callable, Dict, Iterable, List, Set

import networkx as nx
from networkx import MultiDiGraph


def id_hash(*args, size: int = 16) -> str:
    seed = "".join(args)
    return sha256(seed.encode()).hexdigest()[0:size]


def id_of_node(label: str):
    # return "id_"+id_hash(label.lower(), size=12)
    return "id_"+re.sub(r"\W", "", label)


class EdgeInTree:
    def __init__(self,
                 child: str,
                 parent: str,
                 attributes: Dict):
        self.child = child
        self.parent = parent
        self.attributes = attributes

    def __str__(self):
        return f"{self.child}->{self.parent} {self.attributes}"

    def to_dict(self):
        return {
            "child": self.child,
            "parent": self.parent,
            "attributes": self.attributes
        }


class BaseTree:
    __root_label__ = "<ROOT>"

    def __init__(self):
        """
        Simple tree with ordered leaves
        """
        self.graph = MultiDiGraph()
        rootlabel = BaseTree.__root_label__
        self.graph.add_node(rootlabel)
        self._checkpoint = rootlabel
        self.map2parents: Dict[str, str] = {}

    @property
    def root(self):
        return BaseTree.__root_label__

    @property
    def checkpoint(self):
        return self._checkpoint

    @checkpoint.setter
    def checkpoint(self, node_id: str):
        self._checkpoint = node_id

    def check(self, node_id: str):
        """
        c.f. the `mount` command
        """
        self.checkpoint = node_id

    def update_parent(self, child: str, parent: str) -> BaseTree:
        self.map2parents[child] = parent

    def update_checkpoint(self, node_id: str):
        self.checkpoint = node_id

    def parent(self, child: str) -> str:
        return self.map2parents[child]

    def add_edge(self, parent: str, child: str) -> BaseTree:
        if not parent:
            parent = self.root
        self.graph.add_edge(parent, child)
        self.update_parent(child=child, parent=parent)
        self.check(node_id=child)

    def update_node_attrs(self, node_attrs: Dict[str, Dict]):
        nx.set_node_attributes(self.graph, node_attrs)

    def append(self, node_id: str) -> BaseTree:
        """
        Right append a new node to the open leaves
        """
        self.add_edge(parent=self.parent(child=self.checkpoint), child=node_id)
        return self

    def grow(self, node_id: str) -> BaseTree:
        """
        Attach the node as a new leaf to the checkpoint
        """
        self.add_edge(parent=self.checkpoint, child=node_id)
        return self

    def leaves(self) -> List[str]:
        """
        Get all nodes which have no outgoing edges
        """
        nodes = [node for node in self.graph.nodes
                 if self.graph.out_degree(node) == 0]
        return nodes

    def walk_from(self, start_nodes: List[str]) -> List[str]:
        """
        Recursively reach all other nodes from the start nodes
        """

        visited = set()
        queue = start_nodes.copy()
        result = []

        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)
                result.append(node)
                neighbors = self.graph.neighbors(node)
                queue.extend(neighbors)

        return result

    def walk(self) -> List[str]:
        self.walk_from(start_nodes=self.root)

    def flatten(self) -> Iterable[Dict]:
        for child, parent in self.map2parents.items():
            parent = parent if parent != self.root else ""
            attrs = self.graph.nodes[child]
            yield EdgeInTree(child=child, parent=parent, attributes=attrs)

    def flatlist(self) -> List[EdgeInTree]:
        return list(self.flatten())

    def print(
        self,
        startfrom: str = None,
        indent=0,
        msg: str = ""
    ):
        startfrom = self.root if not startfrom else startfrom
        _indent = '\t'*indent
        _content = self.graph.nodes[startfrom]
        print(f"{_indent}{startfrom} {_content if _content else ''}")
        for child in self.graph.successors(startfrom):
            self.print(startfrom=child, indent=indent+1)


def test():
    tree1 = BaseTree()
    tree1.grow("A")
    tree1.grow("A1")
    tree1.append("A2")
    tree1.check("A")
    tree1.append("B")
    tree1.grow("B1")
    tree1.append("B2")
    tree1.print()

    tree2 = BaseTree()
    tree2.add_edge(tree2.root, "A")
    tree2.add_edge("A", "A1")
    tree2.add_edge("A", "A2")
    tree2.add_edge(tree2.root, "B")
    tree2.add_edge("B", "B1")
    tree2.add_edge("B", "B2")
    tree2.update_node_attrs(node_attrs={"B2": {"type": "foo"}})
    tree2.update_node_attrs(
        node_attrs={"B2": {"image": "bar", "color": "red"}})
    tree2.print()
    for i in tree2.flatlist():
        print(i.to_dict())


if __name__ == "__main__":
    test()
