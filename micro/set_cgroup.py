import os
import sys
import time

import yaml

namespace = ['zxz-text']
AllPod = []
NodeCPU = {'skv-node2': 0, 'skv-node3': 0, 'skv-node4': 0, 'skv-node5': 0, 'skv-node6': 0, 'skv-node7': 0}


 

def get_CPU(num: int):
    if num < 20:
        return num * 4 + 1, num * 4 + 3
    else:
        return (num - 20) * 4, (num - 20) * 4 + 2


 

def get_CPU_one(num: int):
    if num < 20:
        return num
    else:
        return num

while True:
    pod_info = ''.join(os.popen(f"kubectl get pod -n wrk-nginx -o wide | grep Running | awk '{{print $1,$7}}'")).split()
    if len(pod_info) == 2 * (int(sys.argv[1]) + int(sys.argv[2])):
        break
    else:
        print('wait all the Pod is Running')
        time.sleep(1)

for ns in namespace:
    pod_node_list = ''.join(os.popen("kubectl get pod -o wide -n " + ns
                                     + " | grep Running | awk '{print $1,$7}'")).split()
    print(pod_node_list)
    for pod_i in range(int(len(pod_node_list) / 2)):
        AllPod.append(ns + '~' + pod_node_list[2 * pod_i] + '~' + pod_node_list[2 * pod_i + 1])

special = ['mongodb', 'memcached', 'redis']
q = 0
for i in AllPod:
    q += 1
    ns, pod, node = i.split('~')
    flag = 0
    for spe in special:
        if spe in pod:
            flag = 1
    cpus = ''
    if flag == 0:
        a = NodeCPU[node]
        NodeCPU[node] = NodeCPU[node] + 1
        cpus += str(a)
        print(f"ssh {node} 'sh /tmp/cgroup.sh {pod} {cpus}'")
        os.system(f"ssh {node} 'sh /tmp/cgroup.sh {pod} {cpus}'")
