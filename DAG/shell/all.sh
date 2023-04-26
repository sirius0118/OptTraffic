
cd /home/k8s/exper/zxz/MSScheduler_python/DAG/shell

mkdir /home/k8s/exper/zxz/MSScheduler_python/DAG/results/result
mkdir /home/k8s/exper/zxz/MSScheduler_python/DAG/results/result/adapt
mkdir /home/k8s/exper/zxz/MSScheduler_python/DAG/results/result/test

for qps in 500 1000 1500 2000 2500 3000 3500 4000; do
    for i in 1 2 3 4 5; do
        for j in random restrict our; do
            sh ./once.sh $j $i $qps
        done
    done
done

mv /home/k8s/exper/zxz/MSScheduler_python/DAG/results/result /home/k8s/exper/zxz/MSScheduler_python/DAG/results/result1.17
