#!/bin/bash

set -x

# $1== 需要重定向的pod
# $2== 重定向的目标service
# eg: A->B->C; kubectl exec -n nginx-app app-b -- /redirect.sh service-c
# pod-A中执行 curl http://service-b:80/redirect/ 

kubectl exec -n nginx-app $1 -- /redirect.sh $2