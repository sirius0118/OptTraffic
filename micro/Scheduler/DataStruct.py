import os
from typing import List, Dict


class Pod:
    def __init__(self, name, NodeName):
        self.Name = name
        self.deploy = None
        self.NodeName = NodeName
        if 'wrk' in self.Name:
            self.deploy = 'wrk'
        else:
            self.deploy = 'nginx'


class PodSet:
    def __init__(self):
        self.Pods: Dict[str, Pod] = {}
        self.wrk: List[Pod] = []
        self.nginx: List[Pod] = []

    def DSInit(self):
        pod_info = ''.join(os.popen(f"kubectl get pod -n wrk-nginx -o wide | awk '{{print $1,$7}}' | sed '1d'")).split()
        for i in range(int(len(pod_info) / 2)):
            self.Pods[pod_info[i * 2]] = Pod(pod_info[i * 2], pod_info[i * 2 + 1])
            if 'wrk' in pod_info[i * 2]:
                self.wrk.append(self.Pods[pod_info[i * 2]])
            elif 'nginx' in pod_info[i * 2]:
                self.nginx.append(self.Pods[pod_info[i * 2]])


class Node:
    def __init__(self, name):
        self.Name = name
        self.wrk: List[Pod] = []
        self.nginx: List[Pod] = []
        self.Ratio: Dict[Pod, float] = {}


class NodeSet:
    def __init__(self):
        self.NodeSet: Dict[str, Node] = {}
        self.NodeNames: List[str] = []

    def DSInit(self, pods: PodSet):
        for pod in pods.Pods.keys():
            if pod not in self.NodeNames:
                self.NodeNames.append(pod)
        for i in self.NodeNames:
            self.NodeSet[i] = Node(i)
        for pod in pods.Pods.keys():
            if pods.Pods[pod].deploy == 'wrk':
                self.NodeSet[pods.Pods[pod].NodeName].wrk.append(pods.Pods[pod])
            elif pods.Pods[pod].deploy == 'nginx':
                self.NodeSet[pods.Pods[pod].NodeName].nginx.append(pods.Pods[pod])
            self.NodeSet[pods.Pods[pod].NodeName].Ratio[pods.Pods[pod]] = 1 / len(pods.nginx)

