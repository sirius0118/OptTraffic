import sys

with open('/home/k8s/exper/zxz/MSScheduler_python/micro/Scheduler/qps', 'r') as f:
    qps = int(f.read())

print(int(qps / int(sys.argv[1])))
