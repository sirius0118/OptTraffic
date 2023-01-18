import os

def get_node_cpu_spend(node):
    result = []
    for node_i in node:
        data = ''.join(os.popen(f"kubectl describe node {node_i} | grep cpu | grep %"))
        per = data[data.index('(') + 1:data.index('%')]
        result.append(int(per))
    return result


with open('/home/k8s/exper/zxz/MSScheduler_python/MSDeScheduler/strategy/percent.txt', 'w') as f:
    for i in get_node_cpu_spend(['skv-node2', 'skv-node3', 'skv-node4', 'skv-node6', 'skv-node7']):
        f.write(str(i) + ',')
    
    f.write('\n20\n')
