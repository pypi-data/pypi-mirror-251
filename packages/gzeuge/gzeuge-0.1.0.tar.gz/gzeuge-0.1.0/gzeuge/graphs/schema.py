from typing import Dict, List, Set, Type

from pydantic import BaseModel


class NodeAttributes(BaseModel):
    label: str
    shape: str
    category: str


class OrdinaryNode(BaseModel):
    hash: str
    attributes: NodeAttributes


class OrdinaryEdge(BaseModel):
    source: str
    target: str
    attributes: Dict = {}


class GraphProps(BaseModel):
    label: str
