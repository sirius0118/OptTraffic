#!/usr/bin/env bash

 

cd /home/k8s/exper/zxz/MSScheduler_python
if [ "$1" == "random" ];then
  python3 MSCreater.py social-network create &
  python3 MSCreater.py media-microservice create
else
  python3 MSCreater.py social-network &
  python3 MSCreater.py media-microservice
fi


#python3 MSCreater.py hotel-reservation create

sleep 100s
 
IP
social_ip=$(kubectl -n social-network get svc nginx-thrift | awk '{print $3}' | sed -n '2p')
#hotel_ip=$(kubectl -n hotel-reservation get svc frontend | awk '{print $3}' | sed -n '2p')
media_ip=$(kubectl -n media-microsvc get svc nginx-web-server | awk '{print $3}' | sed -n '2p')

 

cd /home/k8s/exper/zxz/DeathStarBench/socialNetwork
python3 scripts/init_social_graph.py --ip="$social_ip" &

cd /home/k8s/exper/zxz/DeathStarBench/hotelReservation
#python3 scripts/init_social_graph.py --ip=$social_ip

cd /home/k8s/exper/zxz/DeathStarBench/mediaMicroservice
python3 scripts/write_movie_info.py --server_address http://"$media_ip":8080

for i in {1..1000} ; do
    # shellcheck disable=SC2027
    curl -d "first_name=first_name_""$i""&last_name=last_name_""$i""&username=username_""$i""&password=password_""$i" \
      http://"$media_ip":8080/wrk2-api/user/register
done

sleep 100s
 

echo "start initiation test"

 

/home/k8s/exper/zxz/DeathStarBench/socialNetwork/wrk2/wrk -t 2 -c 20 -d 200s -R 1500 --latency -s /home/k8s/exper/zxz/DeathStarBench/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://"$social_ip":8080 &
#/home/k8s/exper/zxz/DeathStarBench/hotelReservation/wrk2/wrk -t 2 -c 20 -d 200s -R 1000 --latency -s /home/k8s/exper/zxz/DeathStarBench/hotelReservation/wrk2/scripts/mixed-workload_type_1.lua http://"$hotel_ip":5000 &
/home/k8s/exper/zxz/DeathStarBench/mediaMicroservice/wrk2/wrk -t 2 -c 20 -d 200s -R 1500 --latency -s /home/k8s/exper/zxz/DeathStarBench/mediaMicroservice/wrk2/scripts/media-microservices/compose-review.lua http://"$media_ip":8080

 

sleep 100s
/home/k8s/exper/zxz/DeathStarBench/socialNetwork/wrk2/wrk -t 2 -c 20 -d 300s -R 1500 --latency -s /home/k8s/exper/zxz/DeathStarBench/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://"$social_ip":8080 &
#/home/k8s/exper/zxz/DeathStarBench/hotelReservation/wrk2/wrk -t 2 -c 20 -d 200s -R 1000 --latency -s /home/k8s/exper/zxz/DeathStarBench/hotelReservation/wrk2/scripts/mixed-workload_type_1.lua http://"$hotel_ip":5000 &
/home/k8s/exper/zxz/DeathStarBench/mediaMicroservice/wrk2/wrk -t 2 -c 20 -d 300s -R 1500 --latency -s /home/k8s/exper/zxz/DeathStarBench/mediaMicroservice/wrk2/scripts/media-microservices/compose-review.lua http://"$media_ip":8080 &

sleep 250s

echo "start $1"

if [ "$1" == "baseline" ] || [ "$1" == "our" ]; then
  echo "run"
  cd /home/k8s/exper/zxz/MSScheduler_python
  python3 MSDeScheduler.py "$1"
else
  sleep 100s
fi

sleep 60s

 

/home/k8s/exper/zxz/DeathStarBench/socialNetwork/wrk2/wrk -t 2 -c 20 -d 300s -R 1500 --latency -s /home/k8s/exper/zxz/DeathStarBench/socialNetwork/wrk2/scripts/social-network/compose-post.lua http://"$social_ip":8080 &
#/home/k8s/exper/zxz/DeathStarBench/hotelReservation/wrk2/wrk -t 2 -c 20 -d 300s -R 2000 --latency -s /home/k8s/exper/zxz/DeathStarBench/hotelReservation/wrk2/scripts/mixed-workload_type_1.lua http://"$hotel_ip":5000 &
/home/k8s/exper/zxz/DeathStarBench/mediaMicroservice/wrk2/wrk -t 2 -c 20 -d 300s -R 1500 --latency -s /home/k8s/exper/zxz/DeathStarBench/mediaMicroservice/wrk2/scripts/media-microservices/compose-review.lua http://"$media_ip":8080 &

 

# shellcheck disable=SC2164
sleep 300s
cd /home/k8s/exper/zxz/MSScheduler_python/experiment/python
python3 get_bandwidth.py "$1"

 

sleep 400s
cd /home/k8s/exper/zxz/MSScheduler_python
python3 MSCreater.py social-network delete
python3 MSCreater.py media-microservice delete

sleep 100s
