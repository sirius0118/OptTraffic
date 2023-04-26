#!/bin/bash

set -x

wrk_pods=$(kubectl get pods -n wrk-nginx -owide | grep Running | grep wrk | awk '{print $1}')

# $1==connections
# $2==duration
# $3==threads
# $4==body size

for wrk_pod in $wrk_pods
do
    kubectl exec -n wrk-nginx $wrk_pod -- /wrk.sh $1 $2 $3 $4 &
done