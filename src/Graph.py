from typing import Any
from .Node import Node


class Graph:
    def __init__(self) -> None:
        self.nodes: list[Node] = []

    def add_node(self, node: Node) -> None:
        self.nodes.append(node)

    def info(self) -> None:
        print(f"Number of nodes: {len(self.nodes)}\n")
        print("Nodes:")

        for node in self.nodes:
            print(f"name: {node.name}\nposition: {node.pos}\nmeta datas: {node.meta_data}\n")