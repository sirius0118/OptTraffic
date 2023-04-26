import os
import sys


def get_node_cpu_spend(node):
    result = []
    for node_i in node:
        data = ''.join(os.popen(f"kubectl describe node {node_i} | grep cpu | grep %"))
        per = data[data.index('(')+1:data.index('%')]
        result.append(int(per))
    return result


node = ['skv-node2', 'skv-node3', 'skv-node4', 'skv-node5', 'skv-node6', 'skv-node7']

result = get_node_cpu_spend(node)

f = open("/home/k8s/exper/zxz/MSScheduler_python/DAG/results/result/CPU_usage.txt", 'a')
f.write("Type\tNodeName\tCPU usage\n")
for i in node:
    f.write(f"{sys.argv[1]}\t{i}\t{str(result[node.index(i)])}\n")
f.write('\n')
f.close()
