#! /bin/bash
# Creates the system and obtains metrics based on
# number of nodes ($1) and petitions ($2) and threads ($3)

# Check that exactly two arguments are provided
if [ "$#" -ne 2 ]; then
	echo "Usage: $0 <Nodes 1-4> <Petitions 100-20000>"
	exit 1
fi

nodes=$1
petitions=$2

if ! [[ "$nodes" =~ ^[0-9]+$ ]] || [ "$nodes" -lt 1 ] || [ "$nodes" -gt 8 ]; then
	echo "Error: Nodes must be an integer between 1 and 4"
	exit 1
fi

if ! [[ "$petitions" =~ ^[0-9]+$ ]] || [ "$petitions" -lt 100 ] || [ "$petitions" -gt 20000 ]; then
	echo "Error: Petitions must be an integer between 100 and 20000"
	exit 1
fi


# First we deploy redis
sudo docker run --name InsultRedis -d -p 6379:6379 redis

# First we deploy pika
# Wait for RabbitMQ to start inside the container
sudo docker run --name InsultRabbitmq -d -p 5672:5672 -p 15672:15672 rabbitmq:management

sleep 10

# Open new node with Insult Producer
python3 InsultClient.py & 
insult_producer=$(echo $!)

# Open new nodes with Suscribers
python3 Subscriber.py & 
subscriber1=$(echo $!)
python3 Subscriber.py & 
subscriber2=$(echo $!)

# Open new node with Event Publisher
python3 EventPublisher.py & 
event_publisher=$(echo $!)

# Open new node with Insult Filter Producer
python3 InsultFilterClient.py "$petitions" &
insult_filter_producer=$(echo $!)

echo "Time with '"${nodes}"' nodes and '"${petitions}"' petitions." 1>> time_log

insult_filter_pids=()

for ((i=0; i<$nodes; i++)); do
	python3 InsultFilterService.py "$petitions" &
	pid=$!
	insult_filter_pids+=("$pid")
done

# Open new node that checks end of test
python3 EndChecker.py 1>> time_log &
end_checker=$(echo $!)

wait $end_checker

echo "I end end checker"

wait $insult_producer
kill $subscriber1
kill $subscriber2
kill $event_publisher
wait $insult_filter_producer

for pid in "${insult_filter_pids[@]}"; do
    kill $pid
done

sudo docker stop InsultRedis
sudo docker stop InsultRabbitmq
sudo docker rm InsultRedis
sudo docker rm InsultRabbitmq
