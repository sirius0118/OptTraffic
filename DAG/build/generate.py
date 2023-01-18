import json
import yaml

from set_para import gen_lua

f = open("/home/k8s/exper/zxz/MSScheduler_python/DAG/build/graph.json", 'r')
data = json.load(f)
f.close()



yaml_file = []
for k in data['topo'].keys():
    
    gen_lua(k, data['meta'][k][0], data['meta'][k][1], data['meta'][k][2], data['topo'][k])
    f = open("/home/k8s/exper/zxz/MSScheduler_python/DAG/build/app.yaml", 'r')
    tmpos = yaml.load_all(f.read(), Loader=yaml.FullLoader)
    f.close()
    for tmpo in tmpos:
        # print(tmpo)
        if tmpo['kind'] == 'Service':
            tmpo['metadata']['labels']['app-name'] = k
            tmpo['metadata']['name'] = k
            tmpo['spec']['selector']['app-name'] = k
        if tmpo['kind'] == 'Deployment':
            tmpo['metadata']['labels']['app-name'] = k
            tmpo['metadata']['name'] = k
            tmpo['spec']['replicas'] = data['meta'][k][3]
            # tmpo['spec']['selector']['app-name'] = k
            tmpo['spec']['selector']['matchLabels']['app-name'] = k
            tmpo['spec']['template']['metadata']['labels']['app-name'] = k
            tmpo['spec']['template']['metadata']['name'] = k
            tmpo['spec']['template']['spec']['containers'][0]['name'] = k
            tmpo['spec']['template']['spec']['volumes'][0]['hostPath']['path'] = '/tmp/' + k + '.lua'
        yaml_file.append(tmpo.copy())

with open("/home/k8s/exper/zxz/MSScheduler_python/DAG/build/DAG.yaml", 'w') as f:
    yaml.dump_all(yaml_file, f)