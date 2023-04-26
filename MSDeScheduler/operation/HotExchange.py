import os
import sys
import time
from typing import Dict, List
import yaml
import copy
import threading
from ..kube_tool.kubectl import get_PODList_namespace
from MSDeScheduler.metrics.TrafficGraph import Graph, Vertices, GraphSet
from MSDeScheduler.metrics.ClusterStatus import NodeStatus, NodeStatusSet


def get_node_cpu_spend(node_i):
    data = ''.join(os.popen(f"kubectl describe node {node_i} | grep cpu | grep %"))
    per = data[data.index('(')+1:data.index('%')]
    result = int(per)
    return result

class operate:
    def __init__(self, graphSet: GraphSet, graph: Graph, nodeStatusSet: NodeStatusSet):
        self.node_lock = 0
        self.graphSet = graphSet
        self.graph = graph
        self.nodeStatusSet = nodeStatusSet
         

        self.result = graphSet.serviceEdge
        # for i in self.nodeStatusSet.NodeSet.keys():
        #     for j in self.nodeStatusSet.NodeSet[i].FreedomPod:
        #         print(i, '   ', j.Name)

     
Pod 
    def ExecuteMovePod(self, targetPod: Vertices, targetNode: str):
        if get_node_cpu_spend(targetNode) > 95:
            return False
        yaml_path = './MSDeScheduler/tmp/temp/'
        times = 0
        deploy = ''
        for i in range(len(targetPod.Name) - 1, 0, -1):
            if targetPod.Name[i] == '-':
                deploy = targetPod.Name[:i]
                times += 1
                if times == 2:
                    break
        targetPod.NodeName = targetNode
        print('Execute 接收到的参数  ', targetPod.Name, targetNode)
        _ = ''.join(os.popen(f"kubectl get deployment -o yaml -n {targetPod.MSName} "
                             f"{deploy} > {yaml_path}{targetPod.MSName}-{targetPod.Name}.yaml"))
        time.sleep(1)
        result, temp = [], []
        with open(f"{yaml_path}{targetPod.MSName}-{targetPod.Name}.yaml", encoding='utf-8') as f:
            docs = yaml.load_all(f.read(), Loader=yaml.FullLoader)
            for doc in docs:
                tem = copy.deepcopy(doc)
                 
。用户启动一个新的Deployment
                tem['metadata']['name'] = tem['metadata']['name'] + 'add'
                add_pod = doc['metadata']['name']
                tem['spec']['template']['spec']['nodeName'] = targetNode
                doc['spec']['template']['spec']['nodeName'] = targetNode
                temp.append(tem)
                result.append(doc)
        os.system(f"rm {yaml_path}{targetPod.MSName}-{targetPod.Name}.yaml")
        with open(f"{yaml_path}temp-{targetPod.MSName}-{targetPod.Name}.yaml", 'w') as f:
            yaml.dump_all(temp, f)
        with open(f"{yaml_path}{targetPod.MSName}-{targetPod.Name}.yaml", 'w') as f:
            yaml.dump_all(result, f)

        def startPod(tarPod: Vertices, path, add):
            print('生成add')
            _ = ''.join(os.popen(f"kubectl apply -f {path}temp-{tarPod.MSName}-{tarPod.Name}.yaml"))
            while True:
                if "Running" in ''.join(os.popen("kubectl get pod -n " + tarPod.MSName
                                                 + " | grep " + add + "add- | awk '{print $3}'"))[:-1]:
                    _ = ''.join(os.popen(f"kubectl delete deployment -n {tarPod.MSName} {add}"
                                         f" --force --grace-period=0"))
                    break
                time.sleep(1)
            print('生成本体')
            _ = ''.join(os.popen(f"kubectl apply -f {path}{tarPod.MSName}-{tarPod.Name}.yaml"))
            while True:
                if "Running" in ''.join(os.popen("kubectl get pod -n " + tarPod.MSName
                                                 + " | grep " + add + "- | awk '{print $3}'"))[:-1]:
                    _ = ''.join(os.popen(f"kubectl delete deployment -n {tarPod.MSName} {add}add"
                                         f" --force --grace-period=0"))
                    break
                time.sleep(1)
        print('准备start execute')
        startPod(targetPod, yaml_path, add_pod)
        # del targetPod

        # Pod迁移之后需要修改vertice的数据结构，修改其中的name和nodename
        pods = get_PODList_namespace(targetPod.MSName)
        service_name = targetPod.ServiceName
        old_pods = [i.Name for i in self.graphSet.GraphSet[targetPod.MSName].ServiceSet[service_name]]
        new_pods = []
        for i in pods:
             
servicename 与 i 的前前面相同， 
            if service_name == i[:len(service_name)]:
                new_pods.append(i)
        new_pod = None
        for i in new_pods:
            if i not in old_pods:
                new_pod = i
                break
        old_pod = None
        for i in old_pods:
            if i not in new_pods:
                old_pod = i
                break
        # print(old_pos, new_pods)
         
Pod可能会跟之前的Pod重名，因此会报错。 
        print('新的Pod new_pod:', new_pod)
        targetPod.NodeName = targetNode
         
，然后将新数据结构索引上去。最后修改新数据中的Name值

        if new_pod is not None:
            del self.graphSet.GraphSet[targetPod.MSName].VerticesSet[targetPod.Name]
            self.graphSet.GraphSet[targetPod.MSName].VerticesSet[new_pod] = targetPod
            targetPod.Name = new_pod
            targetPod.NodeName = targetNode

        # start = threading.Thread(target=startPod, args=(f"{yaml_path}", add_pod, delete_pod))
        # start.start()

    def HotExchange(self, already: Dict[str, List[str]], targetPod: Vertices, matchPod: str, targetNode: str, ratio: float):
        """
        当需要移动某容器时， 
        为了实现热交换，需要修改nodeStatus数据结构，并且生成真实移动决定并调用ExecuteMovePod。
        :return:
        """
        
        source_node = targetPod.NodeName
        changePod = None
        standby: Dict[float, List[Vertices]] = {}
        # TODO:不能完全使用CPU。 
        #  量最小的。初代版本也是可以纯依赖CPU的
         
FreedomPod。
         
CPU request中与targetPod最接近的，若有多个则从其中找出一个最能保证两台机器CPU 
        # while True:
        #     if self.node_lock == 0:
        #         break
        self.node_lock = 1
        if len(self.nodeStatusSet.NodeSet[targetNode].FreedomPod) != 0:
            for pod in self.nodeStatusSet.NodeSet[targetNode].FreedomPod:
                 
 Pod 不能与当前 Pod 属于同一个 Service
                if pod.ServiceName != targetPod.ServiceName \
                        and pod.ServiceName != matchPod and not pod.Stateful:
                    if abs(pod.CPU_request - targetPod.CPU_request) not in standby.keys():
                        standby[abs(pod.CPU_request - targetPod.CPU_request)] = [pod]
                    else:
                        standby[abs(pod.CPU_request - targetPod.CPU_request)].append(pod)
        # self.node_lock = 0
        standby_key = list(standby.keys())
        standby_key.sort()
        flag = 0
        for i in range(len(standby.keys())):
            if len(standby[standby_key[i]]) == 1:
                if standby[standby_key[i]][0].Stateful:
                    continue
                elif 'add' not in standby[standby_key[i]][0].Name:
                    if standby[standby_key[i]][0].ServiceName not in already:
                            changePod = standby[standby_key[i]][0]
                            flag = 1
                            break
                    # for j in self.result:
                    #     if standby[standby_key[i]][0].ServiceName not in j:
                    #         changePod = standby[standby_key[i]][0]
                    #         flag = 1
                    #         break
            else:
                abs_value = []
                for pod in standby[standby_key[i]]:
                    if not pod.Stateful:
                        # print('if yes')
                        abs_value.append(abs(self.nodeStatusSet.NodeSet[source_node].CPU_used
                                             - self.nodeStatusSet.NodeSet[targetNode].CPU_used + 2 * pod.CPU_used))
                        # print('append yes')
                if len(abs_value) != 0:
                    if 'add' not in standby[standby_key[i]][abs_value.index(min(abs_value))].Name:
                        if standby[standby_key[i]][abs_value.index(min(abs_value))].ServiceName not in already:
                            changePod = standby[standby_key[i]][abs_value.index(min(abs_value))]
                            flag = 1
                            break
            if flag == 1:
                break
        # Freedom & Matched  
        #  当得到需要迁移Pod时，只需要将Pod从src机器的Matched移动到 tar 
        # print(self.nodeStatusSet.NodeSet[source_node].MatchedPod)
        if isinstance(self.graphSet.GraphSet[targetPod.MSName].GraphTopology[targetPod.ServiceName], List):
            if matchPod in self.graphSet.GraphSet[targetPod.MSName].GraphTopology[targetPod.ServiceName]:
                service_service = targetPod.ServiceName + '~' + matchPod
            else:
                service_service = matchPod + '~' + targetPod.ServiceName
        else:
            if matchPod == self.graphSet.GraphSet[targetPod.MSName].GraphTopology[targetPod.ServiceName]:
                service_service = targetPod.ServiceName + '~' + matchPod
            else:
                service_service = matchPod + '~' + targetPod.ServiceName


         
 Pod 从目标主机的 Freedom  
        # print(targetNode, source_node, changePod)
        if changePod is not None or ratio > 0.3:
             
MatchPod数组中需要删除，加到新机器的MatchPod中
            if targetPod in self.nodeStatusSet.NodeSet[source_node].MatchedPod[service_service][0]:
                self.nodeStatusSet.NodeSet[source_node].MatchedPod[service_service][0].remove(targetPod)
                self.nodeStatusSet.NodeSet[targetNode].MatchedPod[service_service][0].append(targetPod)
            if targetPod in self.nodeStatusSet.NodeSet[source_node].MatchedPod[service_service][1]:
                self.nodeStatusSet.NodeSet[source_node].MatchedPod[service_service][1].remove(targetPod)
                self.nodeStatusSet.NodeSet[targetNode].MatchedPod[service_service][1].append(targetPod)
            start1 = threading.Thread(target=self.ExecuteMovePod, args=(targetPod, targetNode))
            print('tar ', targetPod.Name, targetNode)
            start1.start()
            start1.join()
        if changePod is not None:
            print('多线程来热交换', changePod.Name)
            # self.node_lock = 1
            self.nodeStatusSet.NodeSet[targetNode].FreedomPod.remove(changePod)
             
 Pod 插入源主机的 Freedom  
            self.nodeStatusSet.NodeSet[source_node].FreedomPod.append(changePod)
            self.node_lock = 0
        self.node_lock = 0
        if changePod is not None:
            # TODO：若目标机器FreedomPod列表中无Pod，已有的Pod都存在于MatchedPod内。此时需要根据优先级，将部分MatchedPod移动到Freedom内
            start2 = threading.Thread(target=self.ExecuteMovePod, args=(changePod, source_node))
            print('cha ', changePod.Name, source_node)
            start2.start()
            start2.join()

    def HotTrans(self, targetPod: Vertices, targetNode: str):
        """
        当需要移动某容器时， 
        为了实现热交换，需要修改nodeStatus数据结构，并且生成真实移动决定并调用ExecuteMovePod。
        :return:
        """
        self.ExecuteMovePod(targetPod, targetNode)
        # start1 = threading.Thread(target=self.ExecuteMovePod, args=(targetPod, targetNode))
        # start2 = threading.Thread(target=self.ExecuteMovePod, args=(changePod, source_node))
        # start1.start()
        # start1.join()
        # start2.start()
