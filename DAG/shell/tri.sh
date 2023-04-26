
cd /home/k8s/exper/zxz/MSScheduler_python


python3 /home/k8s/exper/zxz/MSScheduler_python/DAG/python/tri_yaml.py

python3 Creater.py DAG apply /home/k8s/exper/zxz/MSScheduler_python/DAG/build/
python3 Creater.py DAG_local apply /home/k8s/exper/zxz/MSScheduler_python/DAG/build/
python3 Creater.py DAG_our apply /home/k8s/exper/zxz/MSScheduler_python/DAG/build/


sleep 10s

random_ip=$(kubectl -n zxz-test get svc app-a | awk '{print $3}' | sed -n '2p')
local_ip=$(kubectl -n zxz-test1 get svc app-a | awk '{print $3}' | sed -n '2p')
our_ip=$(kubectl -n zxz-test2 get svc app-a | awk '{print $3}' | sed -n '2p')


wrk -t 5 -c 50 -R $3 -d 120 --latency http://$random_ip > /home/k8s/exper/zxz/MSScheduler_python/DAG/results/result/adapt/zxz-test_adapt_random_qps"$3"_exp"$2".log &
wrk -t 5 -c 50 -R $3 -d 120 --latency http://$local_ip > /home/k8s/exper/zxz/MSScheduler_python/DAG/results/result/adapt/zxz-test_adapt_baseline_qps"$3"_exp"$2".log &
wrk -t 5 -c 50 -R $3 -d 120 --latency http://$our_ip > /home/k8s/exper/zxz/MSScheduler_python/DAG/results/result/adapt/zxz-test_adapt_our_qps"$3"_exp"$2".log &

sleep 80s

#our
rm /home/k8s/exper/zxz/MSScheduler_python/MSDeScheduler/tmp_DAG/zxz-test.json
cp /home/k8s/exper/zxz/MSScheduler_python/DAG/build/zxz-test_our.json /home/k8s/exper/zxz/MSScheduler_python/MSDeScheduler/tmp_DAG/zxz-test.json
python3 MSDeScheduler.py our &
sleep 2s

#baseline
rm /home/k8s/exper/zxz/MSScheduler_python/MSDeScheduler/tmp_DAG/zxz-test.json
cp /home/k8s/exper/zxz/MSScheduler_python/DAG/build/zxz-test_local.json /home/k8s/exper/zxz/MSScheduler_python/MSDeScheduler/tmp_DAG/zxz-test.json
python3 MSDeScheduler.py restrict &


wait

sleep 10s
# wrk -t 2 -c 10 -R $3 -d 100 --latency http://$entry_ip > /home/k8s/exper/zxz/MSScheduler_python/DAG/results/result/test/zxz-test_test_"$1"_qps"$3"_exp"$2".log

wrk -t 5 -c 50 -R $3 -d 100 --latency http://$random_ip > /home/k8s/exper/zxz/MSScheduler_python/DAG/results/result/test/zxz-test_test_random_qps"$3"_exp"$2".log &
wrk -t 5 -c 50 -R $3 -d 100 --latency http://$local_ip > /home/k8s/exper/zxz/MSScheduler_python/DAG/results/result/test/zxz-test_test_baseline_qps"$3"_exp"$2".log &
wrk -t 5 -c 50 -R $3 -d 100 --latency http://$our_ip > /home/k8s/exper/zxz/MSScheduler_python/DAG/results/result/test/zxz-test_test_our_qps"$3"_exp"$2".log &
sleep 10s
 

cd /home/k8s/exper/zxz/MSScheduler_python/DAG/python
python3 get_bandwidth.py "$1" &
python3 pod_node.py "$1" &
python3 get_cpu_usage.py "$1" &


cd /home/k8s/exper/zxz/MSScheduler_python
sleep 10s 
python3 Creater.py DAG delete /home/k8s/exper/zxz/MSScheduler_python/DAG/build/
python3 Creater.py DAG_local delete /home/k8s/exper/zxz/MSScheduler_python/DAG/build/
python3 Creater.py DAG_our delete /home/k8s/exper/zxz/MSScheduler_python/DAG/build/

sleep 60s

