#!/bin/bash

wrk2_pods=$(kubectl get pods -n nginx-app -owide | grep Running | grep wrk | awk '{print $1}')

# $1==connections
# $2==duration
# $3==threads
# $4==QPS

for wrk2_pod in $wrk2_pods
do
    kubectl exec -n nginx-app $wrk2_pod -- wrk2 -c $1 -d $2 -t $3 -R $4 --latency http://nginx:80 > $5/$wrk2_pod.log &
done