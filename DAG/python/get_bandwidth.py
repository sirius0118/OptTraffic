import requests
import sys
from typing import Dict, List
import pandas as pd


url_r = "http://127.0.0.1:30090/api/v1/query?query=increase(node_network_receive_bytes_total{device='flannel.1'}[300s])"
url_t = "http://127.0.0.1:30090/api/v1/query?query=increase(node_network_receive_bytes_total{device='flannel.1'}[300s])"
# rate(node_network_receive_bytes_total{instance=~'$node',device=~"$device"}[$interval])*8

# node_name:[receive, transmit]
node_bandwidth: Dict[str, List[float]] = {}
response = requests.request('GET', url_r)
result = response.json()
result = result['data']['result']
# print(result)
for i in result:
    node_bandwidth[i['metric']['instance']] = [float(i['value'][1]) / 300, 0]

response = requests.request('GET', url_t)
result = response.json()
result = result['data']['result']
for i in result:
    node_bandwidth[i['metric']['instance']][1] = float(i['value'][1]) / 300


with open('/home/k8s/exper/zxz/MSScheduler_python/DAG/results/result/bandwidth.txt', 'a') as f:
    f.write('\nType\tNodeName\treceive\ttransmit\n')
    for i in node_bandwidth.keys():
        f.write(f"{sys.argv[1]}\t{i}\t{node_bandwidth[i][0]}\t{node_bandwidth[i][1]}\n")

