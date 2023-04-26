import os
import sys


namespace = ['zxz-test']
node_pod = {}
for ns in namespace:
    pod_node_info = ''.join(os.popen(f"kubectl get pod -owide -n {ns} | awk '{{print $1,$7}}' | sed '1d'")).split()
    for i in range(int(len(pod_node_info) / 2)):
        if pod_node_info[i * 2 + 1] not in node_pod.keys():
            node_pod[pod_node_info[i * 2 + 1]] = [pod_node_info[i * 2]]
        else:
            node_pod[pod_node_info[i * 2 + 1]].append(pod_node_info[i * 2])

f = open("/home/k8s/exper/zxz/MSScheduler_python/DAG/results/result/node_pod.txt", 'a')
f.write("Type\tNodeName\tNumberOfPods\tPods\n")
for node in node_pod.keys():
    f.write(f"{sys.argv[1]}\t{node}\t{len(node_pod[node])}\t{str(node_pod[node])}\n")
f.write('\n')
f.close()



