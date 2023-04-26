import os
import yaml

namespace = ['social-network', 'media-microsvc', 'social-network1', 'media-microsvc1', 'hotel-reservation']
AllPod = []
NodeCPU = {'skv-node2': 0, 'skv-node3': 0, 'skv-node4': 0, 'skv-node6': 0, 'skv-node7': 0}


 

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


for ns in namespace:
    pod_node_list = ''.join(os.popen("kubectl get pod -o wide -n " + ns + " | awk '{print $1,$7}' | sed '1d'")).split()
    print(pod_node_list)
    for pod_i in range(int(len(pod_node_list) / 2)):
        AllPod.append(ns + '~' + pod_node_list[2 * pod_i] + '~' + pod_node_list[2 * pod_i + 1])

special = {'user-timeline-mongodb': 8, "movie-review-mongodb": 8, 'user-review-mongodb': 8}
q = 0
for i in AllPod:
    q += 1
    ns, pod, node = i.split('~')
    flag = 0
    for spe in special.keys():
        if spe in pod:
            flag = special[spe]
    cpus = ''
    # if flag == 0:
    #     a, b = get_CPU(NodeCPU[node])
    #     NodeCPU[node] += 1
    #     cpus += str(a) + ',' + str(b)
    # else:
    #     for j in range(flag):
    #         a, b = get_CPU(NodeCPU[node])
    #         NodeCPU[node] += 1
    #         if j == flag - 1:
    #             cpus += str(a) + ',' + str(b)
    #         else:
    #             cpus += str(a) + ',' + str(b) + ','
    if flag == 0:
        a = get_CPU_one(NodeCPU[node])
        if q % 2 == 0:
            NodeCPU[node] += 1
        cpus += str(a)
    else:
        pass
        # for j in range(flag):
        #     a = get_CPU_one(NodeCPU[node])
        #
        #     NodeCPU[node] += 1
        #     if j == flag - 1:
        #         cpus += str(a)
        #     else:
        #         cpus += str(a) + ','
    os.system(f"ssh {node} 'sh /tmp/cgroup.sh {pod} {cpus}'")
