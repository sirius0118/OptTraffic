import os
import sys

def get_node_cpu_spend(node):
    data = ''.join(os.popen(f"kubectl describe node {node} | grep cpu | grep %"))
    per = data[data.index('(')+1:data.index('%')]
    return int(per)

namespace = ['wrk-nginx']
node_pod = {}
for ns in namespace:
    pod_node_info = ''.join(os.popen(f"kubectl get pod -owide -n {ns} | awk '{{print $1,$7}}' | sed '1d'")).split()
    for i in range(int(len(pod_node_info) / 2)):
        if pod_node_info[i * 2 + 1] not in node_pod.keys():
            node_pod[pod_node_info[i * 2 + 1]] = [pod_node_info[i * 2]]
        else:
            node_pod[pod_node_info[i * 2 + 1]].append(pod_node_info[i * 2])

f = open(sys.argv[1]+"node_pod.txt", 'a')
f.write("\nType\tUM\tDM\tmachine\tNodeName\tCPU usage\tNumberOfPods\tPods\n")
for node in node_pod.keys():
    f.write(f"{sys.argv[2]}\t{sys.argv[3]}\t{sys.argv[4]}\t{sys.argv[5]}"
            f"\t{node}\t{str(get_node_cpu_spend(node))}\t{len(node_pod[node])}\t{str(node_pod[node])}\n")
f.write('\n')
f.close()


