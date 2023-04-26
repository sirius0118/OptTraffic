import os
import sys
import yaml
import time
from typing import Dict, List, Tuple
import requests

percent = 0.65


 
，即CPU申请量达到机器资源的75% 
def check():
    node = ['skv-node2', 'skv-node3', 'skv-node4', 'skv-node6', 'skv-node7']
    url_all = "http://127.0.0.1:30090/api/v1/query?query=kube_node_status_allocatable{resource='cpu'}"
    url_request = "http://127.0.0.1:30090/api/v1/query?query=sum(kube_pod_container_resource_requests{unit='core'})" \
                  " by (node)"

    node_CPU: Dict[str, List[float, float]] = {}
    response = requests.request('GET', url_all)
    result = response.json()
    result = result['data']['result']
    for i in result:
        if i['metric']['node'] in node:
            node_CPU[i['metric']['node']] = [float(i['value'][1]), 0]

    response = requests.request('GET', url_request)
    result = response.json()
    result = result['data']['result']
    for i in result:
        if 'node' in i['metric'].keys():
            if i['metric']['node'] in node:
                node_CPU[i['metric']['node']][1] = float(i['value'][1])

    result = []
    for i in node:
        if node_CPU[i][1] / node_CPU[i][0] < percent:
            result.append(i)
    return result


template = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "name": "nginx",
        "namespace": "others"
    },
    "spec": {
        "containers": [{
            "name": "web",
            "image": "nginx",
            "resources": {
                "limits": {
                    "cpu": "1000m",
                    "memory": "1Gi"
                },
                "requests": {
                    "cpu": "1000m",
                    "memory": '1Gi'
                }
            }
        }]
    }
}

if sys.argv[1] == 'delete':
    os.system('kubectl delete namespace others')
    os.system('kubectl create namespace others')

if sys.argv[1] == 'create':
    ith = 0
    while True:
        result = check()
        print(result)
        if len(result) > 0:
            template['metadata']['name'] = 'nginx-' + str(ith)
            gen = [template]
            with open('/tmp/gen.yaml_file', 'w') as f:
                yaml.dump_all(gen, f)
            os.system('kubectl apply -f /tmp/gen.yaml_file')
        else:
            break
        ith += 1
        if ith > 3:
            break

    print('生成完毕')
