"""
    本文件用于生成随机的副本数量，只对无服务应用生效。DB等Stateful 
"""

import os
import random
import sys
import yaml

path = '/home/k8s/exper/zxz/MSScheduler_python/MSCreater/yaml_read/file/'


def main(argv):
    f = open(path + argv[1], 'r')
    docs = yaml.load_all(f.read(), Loader=yaml.FullLoader)
    f.close()

    key_words = ['mongodb', 'redis', 'memcached', 'sql', 'jaeger']

    result = []
    for doc in docs:
        for k in key_words:
            if k in doc['metadata']['name']:
                result.append(doc)
                break
        doc['spec']['replicas'] = random.randint(1, 5)
        result.append(doc)

    with open(path + argv[1], 'w') as f:
        yaml.dump_all(result, f)


if __name__ == '__main__':
    main(sys.argv)
