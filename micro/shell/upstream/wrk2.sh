#!/bin/bash

wrk2_pods=$(kubectl get pods -n wrk-nginx -owide | grep Running | grep wrk | awk '{print $1}')

# $1==connections
# $2==duration
# $3==threads
# $4==QPS
# $5==body size

for wrk2_pod in $wrk2_pods
do
    kubectl exec -n wrk-nginx $wrk2_pod -- /wrk2.sh $1 $2 $3 $4 $5 &
done