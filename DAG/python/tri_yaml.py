import yaml
import copy

local, our = [], []
with open('/home/k8s/exper/zxz/MSScheduler_python/DAG/build/DAG.yaml', 'r') as f:
    docs = yaml.load_all(f.read(), Loader=yaml.FullLoader)
    
    for doc in docs:
        doc_local = copy.deepcopy(doc)
        doc_our = copy.deepcopy(doc)
        doc_local['metadata']['namespace'] = 'zxz-test1'
        doc_our['metadata']['namespace'] = 'zxz-test2'
        local.append(doc_local)
        our.append(doc_our)


with open('/home/k8s/exper/zxz/MSScheduler_python/DAG/build/DAG_local.yaml', 'w') as f:
    yaml.dump_all(local,  f)
with open('/home/k8s/exper/zxz/MSScheduler_python/DAG/build/DAG_our.yaml', 'w') as f:
    yaml.dump_all(our,  f)