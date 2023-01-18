#!/bin/bash

nginx_pods=$(kubectl get pods -n wrk-nginx -owide | grep nginx | awk '{print $1}')

# $1==index.html size(B)

for nginx_pod in $nginx_pods
do
    kubectl exec -n wrk-nginx $nginx_pod -- /bin/bash /touch.sh $1 &
done