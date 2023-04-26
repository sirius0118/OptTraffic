
cd /home/k8s/exper/zxz/MSScheduler_python


if [ "$1" == "random" ];then
  python3 Creater.py DAG create /home/k8s/exper/zxz/MSScheduler_python/DAG/build/
else
  python3 Creater.py DAG apply /home/k8s/exper/zxz/MSScheduler_python/DAG/build/
fi

sleep 10s

entry_ip=$(kubectl -n zxz-test get svc app-a | awk '{print $3}' | sed -n '2p')


wrk -t 4 -c 96 -R $3 -d 120 --latency http://$entry_ip > /home/k8s/exper/zxz/MSScheduler_python/DAG/results/result/adapt/zxz-test_adapt_"$1"_qps"$3"_exp"$2".log &

sleep 80s

if [ "$1" == "random" ];then
    sleep 20s
else
    python3 MSDeScheduler.py $1
fi

# warm up
wrk -t 4 -c 96 -R $3 -d 100 --latency http://$entry_ip

wrk -t 4 -c 96 -R $3 -d 100 --latency http://$entry_ip > /home/k8s/exper/zxz/MSScheduler_python/DAG/results/result/test/zxz-test_test_"$1"_qps"$3"_exp"$2".log

sleep 10s
 

cd /home/k8s/exper/zxz/MSScheduler_python/DAG/python
python3 get_bandwidth.py "$1" &
python3 pod_node.py "$1" &
python3 get_cpu_usage.py "$1" &


cd /home/k8s/exper/zxz/MSScheduler_python
sleep 10s 
python3 Creater.py DAG delete /home/k8s/exper/zxz/MSScheduler_python/DAG/build/

sleep 60s

