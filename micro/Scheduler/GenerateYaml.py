import copy
import random
import yaml
from typing import Dict, List


def generate(inPath, outPath, result: Dict[str, List[int]], M, N, machines):
     

    YamlDeployment, YamlService, YamlOthers = [], [], []

     
yaml文件转换的map 
    with open(inPath, encoding='utf-8') as f:
        docs = yaml.load_all(f.read(), Loader=yaml.FullLoader)
        for doc in docs:
            if doc['kind'] == 'Service':
                YamlService.append(doc)
                continue
            if doc['kind'] == 'Deployment' or doc['kind'] == 'Pod':
                YamlDeployment.append(doc)
                continue
            YamlOthers.append(doc)

    for deployment in YamlDeployment.copy():
        YamlDeployment.remove(deployment)
        # deployment['metadata']['labels']['MSname'] = MSname
        # deployment['spec']['selector']['matchLabels']['MSname'] = MSname
        # deployment['spec']['template']['metadata']['labels']['MSname'] = MSname
        YamlDeployment.append(deployment)
         
Pod类型或者副本数为1 
        if deployment['kind'] == 'Pod':
            continue
        if deployment['kind'] == 'Deployment':
            if 'wrk' in deployment['metadata']['name']:
                deployment['spec']['replicas'] = M
            else:
                deployment['spec']['replicas'] = N
            if deployment['spec']['replicas'] > 1:
                 

                labels = deployment['metadata']['labels'].copy()
                YamlDeployment.remove(deployment)
                 
，将副本的序号加到标签的最后面。只需要修改Name就好了， 
                replica_number = int(deployment['spec']['replicas'])
                deployment['spec']['replicas'] = 1

                for replica_th in range(replica_number):
                    node_set = ['skv-node2', 'skv-node3', 'skv-node4',  'skv-node6', 'skv-node7']
                    stateful = ['mongodb', 'redis', 'memcached']
                    deployment_copy = copy.deepcopy(deployment)
                    labels_copy = labels.copy()
                    labels_copy['more-replicas'] = 'v' + str(replica_th)
                    # labels_copy['MSname'] = MSname
                    deployment_copy['metadata']['labels'] = labels_copy.copy()
                    deployment_copy['metadata']['name'] += '-' + str(replica_th)

                    value_index = replica_th
                    for i in result.keys():
                        if 'wrk' in deployment['metadata']['name']:
                            flag = 0
                        else:
                            flag = 1
                        if value_index >= result[i][flag]:
                            value_index -= result[i][flag]
                        else:
                            deployment_copy['spec']['template']['spec']['nodeName'] = i
                            break
                        # print(deployment['metadata']['name'], i)
                    # if machine:
                    #     deployment_copy['spec']['template']['spec']['nodeName'] = node_set[
                    #         random.randint(0, machine - 1)]

                    deployment_copy['spec']['selector']['matchLabels'] = labels_copy.copy()
                    deployment_copy['spec']['template']['metadata']['labels'] = labels_copy.copy()
                    YamlDeployment.append(deployment_copy.copy())

    with open(str(outPath) + 'WrkNginx_YamlOthers.yaml', 'w') as f:
        yaml.dump_all(YamlOthers, f)
    with open(str(outPath) + 'WrkNginx_YamlDeployment.yaml', 'w') as f:
        yaml.dump_all(YamlDeployment, f)
    with open(str(outPath) + 'WrkNginx_YamlService.yaml', 'w') as f:
        yaml.dump_all(YamlService, f)


