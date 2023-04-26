import os
import sys
import time
import numpy as np
import copy
from typing import Dict, List, Tuple


class TrafficAllocate:
    def __init__(self):
        self.NameSpace = 'wrk-nginx'
        self.pod_node: Dict[str, str] = {}
        self.edge = {}

     
Pod Name翻译成iptables中对应的SEP Name
    def __PODtoSEP(self, pod: str, service: str):
        print(self.NameSpace, service)
        SVC = ''.join(os.popen("sudo iptables -t nat -nvL KUBE-SERVICES |"
                               " grep " + self.NameSpace + "/" + service + " | awk '{print $3}' | sed -n '2p'"))[:-1]
        SEPs = ''.join(os.popen("sudo iptables -t nat -nvL " + SVC + " | awk '{print $3}' | sed  '1,2d'"))[:-1].split(
            '\n')

        IP = ''.join(
            os.popen("kubectl get pod -o wide -n " + self.NameSpace + " | grep -E '"
                     + pod + ".*Running' | awk '{print $6}'"))[:-1]
        for sep in SEPs:

            ip = ''.join(os.popen("sudo iptables -t nat -nvL " + sep + " | awk '{print $8}' | sed -n '3p'"))[:-1]
            if IP == ip:
                return sep
        return None

    def __PODtoSVC(self, service: str):
        SVC = ''.join(os.popen("sudo iptables -t nat -nvL KUBE-SERVICES |"
                               " grep " + self.NameSpace + "/" + service + " | awk '{print $3}' | sed -n '2p'"))[:-1]
        return SVC

    def __iptables(self):
        """
        :param link: str1~str2
        :return: None
        代表从str1到str2 
        """
        pod_info = ''.join(os.popen(f"kubectl get pod -n wrk-nginx -o wide | grep -E '.* Running' | awk '{{print $1,$7}}'")).split()
        for i in range(int(len(pod_info) / 2)):
            self.pod_node[pod_info[2 * i]] = pod_info[2 * i + 1]

        um_list, dm_list = [], []
        for i in self.pod_node:
            if 'wrk' in i:
                um_list.append(i)
            elif 'nginx' in i:
                dm_list.append(i)
        node_um_dm: Dict[str, List[List[str], List[str]]] = {}
        for i in self.pod_node.keys():
            if i not in node_um_dm.keys():
                node_um_dm[self.pod_node[i]] = [[], []]

        for i in um_list:
            node_um_dm[self.pod_node[i]][0].append(i)
        for i in dm_list:
            node_um_dm[self.pod_node[i]][1].append(i)

        um, dm = np.ones(len(um_list)), np.zeros(len(dm_list))
        need = float(len(um_list)) / float(len(dm_list))
        print('need:', need)
        for node in node_um_dm.keys():
            if len(node_um_dm[node][0]) != 0 and len(node_um_dm[node][1]) != 0:
                if len(node_um_dm[node][0]) / len(node_um_dm[node][1]) >= need:
                    for j in node_um_dm[node][1]:
                        self.edge[node + '~' + j] = need / len(node_um_dm[node][0])
                    for i in node_um_dm[node][0]:
                        for j in node_um_dm[node][1]:
                            um[um_list.index(i)] = um[um_list.index(i)] - need / len(node_um_dm[node][0])
                            dm[dm_list.index(j)] = dm[dm_list.index(j)] + need / len(node_um_dm[node][0])
                 

                else:
                    for j in node_um_dm[node][1]:
                        self.edge[node + '~' + j] = 1 / len(node_um_dm[node][1])
                    for i in node_um_dm[node][0]:
                        for j in node_um_dm[node][1]:
                            um[um_list.index(i)] = um[um_list.index(i)] - 1 / len(node_um_dm[node][1])
                            dm[dm_list.index(j)] = dm[dm_list.index(j)] + 1 / len(node_um_dm[node][1])
        print(self.edge)
        print(1111, node_um_dm)
        print(um, dm)
         
。 
         
dm pod出发，判断哪些dm pod还没有接收到目标流量。然后再判断所有结点内的um pod。若有甚于流量， 
        for dm_i in dm_list:
            if dm[dm_list.index(dm_i)] < need:
                 
um pod有相同的分配比例。适应iptables 
                for node_i in node_um_dm.keys():
                    print(um, dm)
                     

                    if len(node_um_dm[node_i][0]) > 0:
                        if um[um_list.index(node_um_dm[node_i][0][0])] > 0:
                             
。
                            if um[um_list.index(node_um_dm[node_i][0][0])] * len(node_um_dm[node_i][0]) \
                                    <= need - dm[dm_list.index(dm_i)]:
                                dm[dm_list.index(dm_i)] = dm[dm_list.index(dm_i)] \
                                                          + um[um_list.index(node_um_dm[node_i][0][0])] \
                                                          * len(node_um_dm[node_i][0])
                                if um[um_list.index(node_um_dm[node_i][0][0])] > 0:
                                    self.edge[node_i + '~' + dm_i] = um[um_list.index(node_um_dm[node_i][0][0])]
                                for i in node_um_dm[node_i][0]:
                                    um[um_list.index(i)] = 0
                             

                            else:
                                for i in node_um_dm[node_i][0]:
                                    um[um_list.index(i)] = um[um_list.index(i)] \
                                                           - (need - dm[dm_list.index(dm_i)]) \
                                                           / len(node_um_dm[node_i][0])
                                if (need - dm[dm_list.index(dm_i)]) \
                                        / len(node_um_dm[node_i][0]) > 0:
                                    self.edge[node_i + '~' + dm_i] = (need - dm[dm_list.index(dm_i)]) \
                                                                     / len(node_um_dm[node_i][0])
                                dm[dm_list.index(dm_i)] = need
        print(self.edge)


    def ExecuteNode(self):
        self.__iptables()
        print(self.edge)
        sep_ratio = {}
        um, dm = 'wrk', 'nginx'
        svc = self.__PODtoSVC('nginx')
        for node_sep in self.edge.keys():
            node = node_sep[:node_sep.find('~')]
            pod = node_sep[node_sep.find('~') + 1:]
            while True:
                sep = self.__PODtoSEP(pod, dm)
                if sep is not None:
                    break
                time.sleep(1)
            ratio = self.edge[node_sep]
            if node not in sep_ratio.keys():
                sep_ratio[node] = {}
            if sep not in sep_ratio[node].keys():
                sep_ratio[node][sep] = ratio

        print(sep_ratio)
        for node in sep_ratio.keys():
            if not os.path.exists('/tmp/iptables'):
                os.system('mkdir /tmp/iptables')
            if os.path.exists('/tmp/iptables/' + node + '.sh'):
                os.system('rm /tmp/iptables/' + node + '.sh')
            f = open('/tmp/iptables/' + node + '.sh', 'w')
            all_ratio = 1
            for sep in sep_ratio[node].keys():
                if list(sep_ratio[node].keys()).index(sep) == 0:
                    # old = f.read()
                    # f.seek(0)
                    all_ratio = sep_ratio[node][sep]
                    f.write("sudo iptables -t nat -I " + svc + " 1 -s 0.0.0.0/0 -j " + sep + " \n")
                    # f.write(old)
                else:
                    # old = f.read()
                    # f.seek(0)
                    all_ratio += sep_ratio[node][sep]
                    f.write("sudo iptables -t nat -I " + svc + " 1 -s 0.0.0.0/0 -j " + sep +
                            " -m statistic --mode random  --probability " + str(
                        sep_ratio[node][sep] / all_ratio) + " \n")
                    # f.write(old)
                # print(sep_ratio[node][sep], all_ratio)

            f.close()
            print("ssh {node} 'sh /tmp/{node1}.sh'".format(node=node, node1=node))
            os.system('scp /tmp/iptables/{node1}.sh {node2}:/tmp/{node3}.sh'.format(node1=node, node2=node, node3=node))
            os.system("ssh {node} 'sh /tmp/{node1}.sh'".format(node=node, node1=node))
            os.system("ssh {node} 'sh /tmp/{node1}.sh'".format(node=node, node1=node))
            os.system("ssh {node} 'sh /tmp/{node1}.sh'".format(node=node, node1=node))
