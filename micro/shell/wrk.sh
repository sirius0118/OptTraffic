#!/bin/bash

wrk_pods=$(kubectl get pods -n wrk-nginx -owide | grep Running | grep wrk | awk '{print $1}')

# $1==connections
# $2==duration
# $3==threads


for wrk_pod in $wrk_pods
do
    kubectl exec -n wrk-nginx $wrk_pod -- wrk -c$1 -d$2 -t$3 --latency http://nginx:80 > $4/$wrk_pod.log &
done