import os
import yaml
from .DataStruct import NodeSet, PodSet, Pod, Node


class MovePod:
    def __init__(self, nodeSet: NodeSet, podSet: PodSet):
        self.nodeSet = nodeSet
        self.podSet = podSet
        pass

    def move(self, pod: Pod, node: Node):
        pass



