import yaml
import os


Best_weight = {'jaeger.yaml_file': 0, 'media-mongodb.yaml_file': 0, 'post-storage-mongodb.yaml_file': 0, 'social-graph-mongodb.yaml_file': 0,
               'url-shorten-mongodb.yaml_file': 0, 'user-mongodb.yaml_file': 0, 'user-timeline-mongodb.yaml_file': 0,
               'compose-post-service.yaml_file': 0, 'home-timeline-redis.yaml_file': 0, 'home-timeline-service.yaml_file': 0,
               'media-frontend.yaml_file': 0, 'media-memcached.yaml_file': 0, 'media-service.json.yaml_file': 0, 'nginx-thrift.yaml_file': 0,
               'post-storage-memcached.yaml_file': 0, 'post-storage-service.yaml_file': 0, 'social-graph-redis.yaml_file': 0,
               'social-graph-service.yaml_file': 0, 'text-service.yaml_file': 0, 'unique-id-service.yaml_file': 0,
               'url-shorten-memcached.yaml_file': 0, 'url-shorten-service.yaml_file': 0, 'user-memcached.yaml_file': 0,
               'user-mention-service.yaml_file': 0, 'user-service.yaml_file': 0, 'user-timeline-redis.yaml_file': 0,
               'user-timeline-service.yaml_file': 0}

RS_weight = {'jaeger.yaml_file': 0, 'media-mongodb.yaml_file': 1, 'post-storage-mongodb.yaml_file': 0, 'social-graph-mongodb.yaml_file': 1, 'url-shorten-mongodb.yaml_file': 1, 'user-mongodb.yaml_file': 1, 'user-timeline-mongodb.yaml_file': 1, 'compose-post-service.yaml_file': 1, 'home-timeline-redis.yaml_file': 1, 'home-timeline-service.yaml_file': 0, 'media-frontend.yaml_file': 1, 'media-memcached.yaml_file': 1, 'media-service.json.yaml_file': 0, 'nginx-thrift.yaml_file': 0, 'post-storage-memcached.yaml_file': 1, 'post-storage-service.yaml_file': 1, 'social-graph-redis.yaml_file': 1, 'social-graph-service.yaml_file': 1, 'text-service.yaml_file': 0, 'unique-id-service.yaml_file': 0, 'url-shorten-memcached.yaml_file': 1, 'url-shorten-service.yaml_file': 0, 'user-memcached.yaml_file': 0, 'user-mention-service.yaml_file': 0, 'user-service.yaml_file': 1, 'user-timeline-redis.yaml_file': 1, 'user-timeline-service.yaml_file': 0}

Graph_weight = {'jaeger.yaml_file': 0, 'media-mongodb.yaml_file': 0, 'post-storage-mongodb.yaml_file': 0,
                'social-graph-mongodb.yaml_file': 1, 'url-shorten-mongodb.yaml_file': 1, 'user-mongodb.yaml_file': 1,
                'user-timeline-mongodb.yaml_file': 1, 'compose-post-service.yaml_file': 0, 'home-timeline-redis.yaml_file': 1,
                'home-timeline-service.yaml_file': 1, 'media-frontend.yaml_file': 1, 'media-memcached.yaml_file': 1,
                'media-service.json.yaml_file': 0, 'nginx-thrift.yaml_file': 0, 'post-storage-memcached.yaml_file': 0,
                'post-storage-service.yaml_file': 0, 'social-graph-redis.yaml_file': 1, 'social-graph-service.yaml_file': 0,
                'text-service.yaml_file': 0, 'unique-id-service.yaml_file': 0, 'url-shorten-memcached.yaml_file': 1,
                'url-shorten-service.yaml_file': 0, 'user-memcached.yaml_file': 1, 'user-mention-service.yaml_file': 0,
                'user-service.yaml_file': 1, 'user-timeline-redis.yaml_file': 1, 'user-timeline-service.yaml_file': 1}

Bad_weight = {'jaeger.yaml_file': 0, 'media-mongodb.yaml_file': 1, 'post-storage-mongodb.yaml_file': 0, 'social-graph-mongodb.yaml_file': 1,
              'url-shorten-mongodb.yaml_file': 1, 'user-mongodb.yaml_file': 1, 'user-timeline-mongodb.yaml_file': 1,
              'compose-post-service.yaml_file': 1, 'home-timeline-redis.yaml_file': 1, 'home-timeline-service.yaml_file': 0,
              'media-frontend.yaml_file': 1, 'media-memcached.yaml_file': 1, 'media-service.json.yaml_file': 0, 'nginx-thrift.yaml_file': 0,
              'post-storage-memcached.yaml_file': 1, 'post-storage-service.yaml_file': 1, 'social-graph-redis.yaml_file': 1,
              'social-graph-service.yaml_file': 1, 'text-service.yaml_file': 1, 'unique-id-service.yaml_file': 0,
              'url-shorten-memcached.yaml_file': 1, 'url-shorten-service.yaml_file': 0, 'user-memcached.yaml_file': 0,
              'user-mention-service.yaml_file': 0, 'user-service.yaml_file': 1, 'user-timeline-redis.yaml_file': 0,
              'user-timeline-service.yaml_file': 0}

path = './DeathStarBench/socialNetwork/k8s-yaml_file/backend/'
yaml_list = os.listdir(path)
for yaml_name in yaml_list:
    if yaml_name[-5:] != '.yaml_file':
        yaml_list.remove(yaml_name)

data = []
for yaml_name in yaml_list:
    print(path + yaml_name)
    with open(path + yaml_name, encoding='utf-8') as f:
        docs = yaml.load_all(f.read(), Loader=yaml.FullLoader)

    for doc in docs:
        doc['metadata']['namespace'] = 'social1'
        if doc['kind'] == 'Deployment':
            if Best_weight[yaml_name] == 0:
                doc['spec']['template']['spec']['nodeName'] = 'skv-node3'
            else:
                doc['spec']['template']['spec']['nodeName'] = 'skv-node4'
        data.append(doc)

    with open(r'./social1_best_a.yaml_file', 'w') as g:
        yaml.dump_all(data,  g)

path = './DeathStarBench/socialNetwork/k8s-yaml_file/'
yaml_list = os.listdir(path)
for yaml_name in yaml_list:
    if yaml_name[-5:] != '.yaml_file':
        yaml_list.remove(yaml_name)

data = []
for yaml_name in yaml_list:
    print(path + yaml_name)
    with open(path + yaml_name, encoding='utf-8') as f:
        docs = yaml.load_all(f.read(), Loader=yaml.FullLoader)

    for doc in docs:
        doc['metadata']['namespace'] = 'social1'
        if doc['kind'] == 'Deployment':
            if Best_weight[yaml_name] == 0:
                doc['spec']['template']['spec']['nodeName'] = 'skv-node3'
            else:
                doc['spec']['template']['spec']['nodeName'] = 'skv-node4'
        data.append(doc)

    with open(r'./social1_best_b.yaml_file', 'w') as g:
        yaml.dump_all(data,  g)
