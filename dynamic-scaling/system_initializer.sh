#! /bin/bash

python3 -m venv venv
source venv/bin/activate
pip install redis
pip install pika

rm -rf graphs
mkdir graphs

# First we deploy redis
sudo docker run --name InsultRedis -d -p 6379:6379 redis

# First we deploy pika
# Wait for RabbitMQ to start inside the container
sudo docker run --name InsultRabbitmq -d -p 5672:5672 -p 15672:15672 rabbitmq:management

sleep 5

# We also deploy redis observer
#python3 see_redis.py & 
#redis_observer=$(echo $!)

# Then we deploy the autoscaler
gnome-terminal --title="Autoscaler" -- bash -c "python3 autoscaler.py" &
sleep 1
autoscaler=$(ps -aux | grep autoscaler.py | grep -v grep | awk '{print $2}')

echo "Autoscaler is "$autoscaler

sleep 3

# Here we must execute clients
./InsultServicePetitions.sh "InsultService/client.py"
echo "InsultService/client.py metrics ended"

./InsultFilterPetitions.sh "InsultFilterService/client.py"
echo "InsultFilterService/client.py metrics ended"

echo "Waiting for petitions to get processed!!"
sleep 20

echo "Kill autoscaler!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
sleep 10

kill $autoscaler

kill $name_server
#kill $redis_observer

sudo docker stop InsultRedis
sudo docker stop InsultRabbitmq
#sudo docker stop rabbitmq

sudo docker rm InsultRedis
sudo docker rm InsultRabbitmq
#sudo docker rm rabbitmq
