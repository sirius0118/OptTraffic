#!/bin/bash

wrk_pods=$(kubectl get pods -n wrk-nginx -owide | grep Running | grep wrk | awk '{print $1}')

for wrk_pod in $wrk_pods
do
    kubectl exec -n wrk-nginx $wrk_pod -- cat /result.log > $1/$wrk_pod.log
done