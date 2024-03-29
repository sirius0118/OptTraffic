# ！/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import json
import requests
from typing import NewType, Dict, Tuple, List

from .TrafficGraph import Vertices, Graph, GraphSet

path = './tmp'


class NodeStatus:
    def __init__(self, Name):
        self.NodeName = Name
        self.CPU_all = 0
        self.CPU_used = 0
        self.CPU_request = 0
        self.RAM_all = 0
        self.RAM_request = 0
        self.RAM_used = 0
         
NodeStatusSet 
         
Node上已经匹配好的Pod组，尽量不要分散这个组内的Pod
        self.MatchedPod: Dict[str, Tuple[List[Vertices], List[Vertices]]] = {}
         
Node上自由的Pod，可以从这个里面找Pod 
        self.FreedomPod: List[Vertices] = []

     
Node上的一些状态值。 
    def DataStructFlash(self):
        pass

    def add_FreedomPod(self, vertice: Vertices):
        self.FreedomPod.append(vertice)

    def del_FreedomPod(self, vertice: Vertices):
        self.FreedomPod.remove(vertice)

     
， 
    def delNamespace(self, graph: Graph):
        for i in graph.VerticesSet.keys():
            if graph.VerticesSet[i] in self.FreedomPod:
                self.FreedomPod.remove(graph.VerticesSet[i])
        for i in graph.EdgeSet.keys():
            if graph.EdgeSet[i].Name in self.MatchedPod.keys():
                del self.MatchedPod[graph.EdgeSet[i].Name]

     
Freedom数组中将Pod移动到Matched 
    # def FreedomToMatched(self, link: str):
    #     um, dm = link[:link.find('~')], link[link.find('~') + 1:]
    #     um_list, dm_list = [], []
    #     for i in self.FreedomPod:
    #         if um == i.Name:
    #             um_list.append(i)
    #             self.FreedomPod.remove(i)
    #         if dm == i.Name:
    #             dm_list.append(i)
    #             self.FreedomPod.remove(i)
    #     self.MatchedPod[link] = [um_list, dm_list]

     
Matched数组将Pod移动到Freedom 
    def MatchedToFreedom(self, link: str):
        um_list, dm_list = self.MatchedPod[link]
        del self.MatchedPod[link]
        for i in um_list:
            self.FreedomPod.append(i)
        for i in dm_list:
            self.FreedomPod.append(i)

     
FreedomPod中获得与目标容器具有最接近的CPU请求的Pod。
     
CPU还有使用的CPU的量， 
    # TODO:获得与自己CPU消耗差不多的的Pod
    def getClosePod(self, PodCPU: float):
        pass


class NodeStatusSet:
    def __init__(self):
        self.NodeSet: Dict[str, NodeStatus] = {}
        self.NodeNameSet: List[str] = []

    #
    def DataStructInit(self, graphSet: GraphSet):
        self.NodeNameSet = ''.join(os.popen("kubectl get node | awk '{print $1}' | sed '1d'"))[:-1].split('\n')
        for i in self.NodeNameSet:
            self.NodeSet[i] = NodeStatus(i)
         
NodeSet中全部NodeStatus中的FreedomPod和MatchedPod 
         
，就默认全部Pod都是Freedom状态，因此全部添加到FreedomPod 
        for namespace in graphSet.GraphSet.keys():
            for vertice_index in graphSet.GraphSet[namespace].VerticesSet.keys():
                Vertice = graphSet.GraphSet[namespace].VerticesSet[vertice_index]
                # print('namespace:', namespace, '   pod:', Vertice.Name)
                self.NodeSet[Vertice.NodeName].add_FreedomPod(Vertice)
        # flash CPU & memory information in NodeStatus
        urlCPU_memory_all = "http://127.0.0.1:30090/api/v1/query?query=kube_node_status_allocatable{resource='cpu'}" \
                            " or kube_node_status_allocatable{resource='memory'}"
        urlCPU_memory_request = "http://127.0.0.1:30090/api/v1/query?query=sum(kube_pod_container_resource_requests)" \
                                " by (node, resource)"
        urlCPU_used = "http://127.0.0.1:30090/api/v1/query?query=sum(container_cpu_usage_seconds_total) by (node)"
        urlMemory_used = "http://127.0.0.1:30090/api/v1/query?query=sum(container_memory_working_set_bytes) by (node)"
        response = requests.request('GET', urlCPU_memory_all)
        result = response.json()
        result = result['data']['result']
        for i in result:
            if 'node' in i['metric'].keys():
                if i['metric']['resource'] == 'cpu':
                    self.NodeSet[i['metric']['node']].CPU_all = float(i['value'][1])
                elif i['metric']['resource'] == 'memory':
                    self.NodeSet[i['metric']['node']].RAM_all = float(i['value'][1])

        response = requests.request('GET', urlCPU_memory_request)
        result = response.json()
        result = result['data']['result']
        for i in result:
            if 'node' in i['metric'].keys():
                if i['metric']['resource'] == 'cpu':
                    self.NodeSet[i['metric']['node']].CPU_request = float(i['value'][1])
                elif i['metric']['resource'] == 'memory':
                    self.NodeSet[i['metric']['node']].RAM_request = float(i['value'][1])

        response = requests.request('GET', urlCPU_used)
        result = response.json()
        result = result['data']['result']
        for i in result:
            if 'node' in i['metric'].keys():
                self.NodeSet[i['metric']['node']].CPU_used = float(i['value'][1])

        response = requests.request('GET', urlMemory_used)
        result = response.json()
        result = result['data']['result']
        for i in result:
            if 'node' in i['metric'].keys():
                self.NodeSet[i['metric']['node']].RAM_used = float(i['value'][1])
