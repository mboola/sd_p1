#! /bin/bash

python3 -m venv venv
source venv/bin/activate
pip install redis
pip install pika

# First we deploy redis
sudo docker run --name InsultRedis -d -p 6379:6379 redis

# First we deploy pika
# Wait for RabbitMQ to start inside the container
sudo docker run --name InsultRabbitmq -d -p 5672:5672 -p 15672:15672 rabbitmq:management

sleep 5

#sudo docker exec InsultRabbitmq rabbitmqctl add_user ar sar
sleep 1

#sudo docker exec InsultRabbitmq rabbitmqctl set_permissions -p / ar ".*" ".*" ".*"

sleep 1

# Then we start NameServer
python3 NameServer.py &
name_server=$(echo $!)

# Wait some time so server can start correctly
sleep 3

# We also deploy redis observer
#python3 see_redis.py & 
#redis_observer=$(echo $!)

# Then we deploy the autoscaler
gnome-terminal --title="Autoscaler" -- bash -c "python3 autoscaler.py" &
autoscaler=$(ps -aux | grep autoscaler.py | grep -v grep | awk '{print $2}')

sleep 3

# Here we must execute clients
gnome-terminal --title="Client" -- bash -c "python3 InsultService/client.py 10000 > time_client"

./obtain_metrics.sh
echo "metrics ended"

sleep 10
wait $autoscaler

kill $name_server
#kill $redis_observer

sudo docker stop InsultRedis
sudo docker stop InsultRabbitmq
#sudo docker stop rabbitmq

sudo docker rm InsultRedis
sudo docker rm InsultRabbitmq
#sudo docker rm rabbitmq
