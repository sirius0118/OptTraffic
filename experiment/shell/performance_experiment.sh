#!/usr/bin/env bash

# shellcheck disable=SC2164
 

for i in {1..5} ; do
  echo "Experiment $i" >> /home/k8s/exper/zxz/MSScheduler_python/experiment/result/node_pod.txt
  cd /home/k8s/exper/zxz/MSScheduler_python/experiment/shell
  sh ./performance_start.sh random "$i"
  sleep 60

  cd /home/k8s/exper/zxz/MSScheduler_python/experiment/shell
  sh ./performance_start.sh restrict "$i"
  sleep 60


  cd /home/k8s/exper/zxz/MSScheduler_python/experiment/shell
  sh ./performance_start.sh our "$i"
  sleep 60
done


