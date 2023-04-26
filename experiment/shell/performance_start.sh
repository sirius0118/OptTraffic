#!/usr/bin/env bash

 

cd /home/k8s/exper/zxz/MSScheduler_python
if [ "$1" == "random" ];then
  python3 MSCreater.py hotel-reservation create &
  python3 MSCreater.py social-network create &
  python3 MSCreater.py social-network1 create &
  python3 MSCreater.py media-microservice create &
  python3 MSCreater.py media-microservice1 create
else
  python3 MSCreater.py hotel-reservation &
  python3 MSCreater.py social-network &
  python3 MSCreater.py social-network1 &
  python3 MSCreater.py media-microservice &
  python3 MSCreater.py media-microservice1
fi


#python3 MSCreater.py hotel-reservation create

sleep 60s
 
。生成其他Pod 
#cd /home/k8s/exper/zxz/MSScheduler_python/experiment/python
#python3 gen_noise.py create


 
IP
social_ip=$(kubectl -n social-network get svc nginx-thrift | awk '{print $3}' | sed -n '2p')
hotel_ip=$(kubectl -n hotel-reservation get svc frontend | awk '{print $3}' | sed -n '2p')
media_ip=$(kubectl -n media-microsvc get svc nginx-web-server | awk '{print $3}' | sed -n '2p')
social1_ip=$(kubectl -n social-network1 get svc nginx-thrift | awk '{print $3}' | sed -n '2p')
media1_ip=$(kubectl -n media-microsvc1 get svc nginx-web-server | awk '{print $3}' | sed -n '2p')

 


cd /home/k8s/exper/zxz/DeathStarBench/mediaMicroservice
python3 scripts/write_movie_info.py --server_address http://"$media_ip":8080
python3 scripts/write_movie_info.py --server_address http://"$media1_ip":8080

for i in {1..1000} ; do
    # shellcheck disable=SC2027
    curl -d "first_name=first_name_""$i""&last_name=last_name_""$i""&username=username_""$i""&password=password_""$i" \
      http://"$media_ip":8080/wrk2-api/user/register
done
for i in {1..1000} ; do
    # shellcheck disable=SC2027
    curl -d "first_name=first_name_""$i""&last_name=last_name_""$i""&username=username_""$i""&password=password_""$i" \
      http://"$media1_ip":8080/wrk2-api/user/register
done

cd /home/k8s/exper/zxz/DeathStarBench/socialNetwork
python3 scripts/init_social_graph.py --ip="$social_ip"
python3 scripts/init_social_graph.py --ip="$social1_ip"

#cd /home/k8s/exper/zxz/DeathStarBench/hotelReservation
#python3 scripts/init_social_graph.py --ip=$social_ip



sleep 30s
 

echo "start warm"

qps_social=1600
qps_social1=1600
qps_media=1000
qps_media1=1000
qps_hotel=1200

 

/home/k8s/exper/zxz/DeathStarBench/hotelReservation/wrk2/wrk -t 2 -c 20 -d 60s -R $qps_hotel --latency -s /home/k8s/exper/zxz/DeathStarBench/hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua http://"$hotel_ip":5000  > /home/k8s/exper/zxz/MSScheduler_python/experiment/result/Latency/warm/"hotel_warm_""$1""_""$qps_hotel""_ex""$2"".log" &
/home/k8s/exper/zxz/DeathStarBench/socialNetwork/wrk2/wrk -t 2 -c 20 -d 60s -R $qps_social --latency -s /home/k8s/exper/zxz/DeathStarBench/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://"$social_ip":8080 > /home/k8s/exper/zxz/MSScheduler_python/experiment/result/Latency/warm/"social_warm_""$1""_"$qps_social"_ex""$2"".log" &
/home/k8s/exper/zxz/DeathStarBench/mediaMicroservice/wrk2/wrk -t 2 -c 20 -d 60s -R $qps_media --latency -s /home/k8s/exper/zxz/DeathStarBench/mediaMicroservice/wrk2/scripts/media-microservices/compose-review.lua http://"$media_ip":8080 > /home/k8s/exper/zxz/MSScheduler_python/experiment/result/Latency/warm/"media_warm_""$1""_"$qps_media"_ex""$2"".log" &
/home/k8s/exper/zxz/DeathStarBench/socialNetwork/wrk2/wrk -t 2 -c 20 -d 60s -R $qps_social1 --latency -s /home/k8s/exper/zxz/DeathStarBench/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://"$social1_ip":8080 > /home/k8s/exper/zxz/MSScheduler_python/experiment/result/Latency/warm/"social1_warm_""$1""_"$qps_social1"_ex""$2"".log" &
/home/k8s/exper/zxz/DeathStarBench/mediaMicroservice/wrk2/wrk -t 2 -c 20 -d 60s -R $qps_media1 --latency -s /home/k8s/exper/zxz/DeathStarBench/mediaMicroservice/wrk2/scripts/media-microservices/compose-review.lua http://"$media1_ip":8080 > /home/k8s/exper/zxz/MSScheduler_python/experiment/result/Latency/warm/"media1_warm_""$1""_"$qps_media1"_ex""$2"".log"

echo "start adapt"
 

sleep 10s
/home/k8s/exper/zxz/DeathStarBench/hotelReservation/wrk2/wrk -t 2 -c 20 -d 150s -R $qps_hotel --latency -s /home/k8s/exper/zxz/DeathStarBench/hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua http://"$hotel_ip":5000  > /home/k8s/exper/zxz/MSScheduler_python/experiment/result/Latency/adapt/"hotel_adapt_""$1""_""$qps_hotel""_ex""$2"".log" &
/home/k8s/exper/zxz/DeathStarBench/socialNetwork/wrk2/wrk -t 2 -c 20 -d 150s -R $qps_social --latency -s /home/k8s/exper/zxz/DeathStarBench/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://"$social_ip":8080 > /home/k8s/exper/zxz/MSScheduler_python/experiment/result/Latency/adapt/"social_adapt_""$1""_"$qps_social"_ex""$2"".log" &
/home/k8s/exper/zxz/DeathStarBench/mediaMicroservice/wrk2/wrk -t 2 -c 20 -d 150s -R $qps_media --latency -s /home/k8s/exper/zxz/DeathStarBench/mediaMicroservice/wrk2/scripts/media-microservices/compose-review.lua http://"$media_ip":8080 > /home/k8s/exper/zxz/MSScheduler_python/experiment/result/Latency/adapt/"media_adapt_""$1""_"$qps_media"_ex""$2"".log" &
/home/k8s/exper/zxz/DeathStarBench/socialNetwork/wrk2/wrk -t 2 -c 20 -d 150s -R $qps_social1 --latency -s /home/k8s/exper/zxz/DeathStarBench/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://"$social1_ip":8080 > /home/k8s/exper/zxz/MSScheduler_python/experiment/result/Latency/adapt/"social1_adapt_""$1""_"$qps_social1"_ex""$2"".log" &
/home/k8s/exper/zxz/DeathStarBench/mediaMicroservice/wrk2/wrk -t 2 -c 20 -d 150s -R $qps_media1 --latency -s /home/k8s/exper/zxz/DeathStarBench/mediaMicroservice/wrk2/scripts/media-microservices/compose-review.lua http://"$media1_ip":8080 > /home/k8s/exper/zxz/MSScheduler_python/experiment/result/Latency/adapt/"media1_adapt_""$1""_"$qps_media1"_ex""$2"".log" &

sleep 70s

echo "start strategy $1"
if [ "$1" == "restrict" ] || [ "$1" == "our" ]; then
  echo "run"
  cd /home/k8s/exper/zxz/MSScheduler_python
  python3 MSDeScheduler.py "$1" > /home/k8s/exper/zxz/MSScheduler_python/experiment/result/"operation_$1_$2.log"
else
  sleep 100s
fi

sleep 60s

#qps_social=1400
#qps_social1=1400
#qps_media=1000
#qps_media1=1000
#qps_hotel=1200

echo "start test"
 

/home/k8s/exper/zxz/DeathStarBench/hotelReservation/wrk2/wrk -t 2 -c 20 -d 200s -R $qps_hotel --latency -s /home/k8s/exper/zxz/DeathStarBench/hotelReservation/wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua http://"$hotel_ip":5000  > /home/k8s/exper/zxz/MSScheduler_python/experiment/result/Latency/test/"hotel_test_""$1""_""$qps_hotel""_ex""$2"".log" &
/home/k8s/exper/zxz/DeathStarBench/socialNetwork/wrk2/wrk -t 2 -c 20 -d 200s -R $qps_social --latency -s /home/k8s/exper/zxz/DeathStarBench/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://"$social_ip":8080 > /home/k8s/exper/zxz/MSScheduler_python/experiment/result/Latency/test/"social_test_""$1""_"$qps_social"_ex""$2"".log" &
/home/k8s/exper/zxz/DeathStarBench/mediaMicroservice/wrk2/wrk -t 2 -c 20 -d 200s -R $qps_media --latency -s /home/k8s/exper/zxz/DeathStarBench/mediaMicroservice/wrk2/scripts/media-microservices/compose-review.lua http://"$media_ip":8080 > /home/k8s/exper/zxz/MSScheduler_python/experiment/result/Latency/test/"media_test_""$1""_"$qps_media"_ex""$2"".log" &
/home/k8s/exper/zxz/DeathStarBench/socialNetwork/wrk2/wrk -t 2 -c 20 -d 200s -R $qps_social1 --latency -s /home/k8s/exper/zxz/DeathStarBench/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://"$social1_ip":8080 > /home/k8s/exper/zxz/MSScheduler_python/experiment/result/Latency/test/"social1_test_""$1""_"$qps_social1"_ex""$2"".log" &
/home/k8s/exper/zxz/DeathStarBench/mediaMicroservice/wrk2/wrk -t 2 -c 20 -d 200s -R $qps_media1 --latency -s /home/k8s/exper/zxz/DeathStarBench/mediaMicroservice/wrk2/scripts/media-microservices/compose-review.lua http://"$media1_ip":8080 > /home/k8s/exper/zxz/MSScheduler_python/experiment/result/Latency/test/"media1_test_""$1""_"$qps_media1"_ex""$2"".log" &


# shellcheck disable=SC2164
sleep 200s
 

echo "save result"
cd /home/k8s/exper/zxz/MSScheduler_python/experiment/python
python3 get_bandwidth.py "$1" &
python3 pod_node.py "$1" &
python3 get_cpu_usage.py "$1" &

echo "back"
 

sleep 10s
 

#cd /home/k8s/exper/zxz/MSScheduler_python/experiment/python
#python3 gen_noise.py delete

cd /home/k8s/exper/zxz/MSScheduler_python
python3 MSCreater.py hotel-reservation delete
python3 MSCreater.py social-network delete
python3 MSCreater.py media-microservice delete
python3 MSCreater.py social-network1 delete
python3 MSCreater.py media-microservice1 delete
sleep 30s

