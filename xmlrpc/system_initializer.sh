#! /bin/bash
# Creates the system and obtains metrics based on
# number of nodes ($1) and petitions ($2) and threads ($3)

# Check that exactly two arguments are provided
if [ "$#" -ne 3 ]; then
	echo "Usage: $0 <Nodes 1-4> <Petitions 100-5000> <Threads 1-10>"
	exit 1
fi

nodes=$1
petitions=$2
threads=$3

if ! [[ "$nodes" =~ ^[0-9]+$ ]] || [ "$nodes" -lt 1 ] || [ "$nodes" -gt 8 ]; then
	echo "Error: Nodes must be an integer between 1 and 8"
	exit 1
fi

if ! [[ "$petitions" =~ ^[0-9]+$ ]] || [ "$petitions" -lt 100 ] || [ "$petitions" -gt 20000 ]; then
	echo "Error: Petitions must be an integer between 100 and 5000"
	exit 1
fi

if ! [[ "$threads" =~ ^[0-9]+$ ]] || [ "$threads" -lt 1 ] || [ "$threads" -gt 10 ]; then
	echo "Error: Threads must be an integer between 1 and 10"
	exit 1
fi

# Start Name Server
python3 NameServer.py & > /dev/null
name_server=$(echo $!)

# Wait some time so Name Server can start correctly
sleep 1

# Start both Raw and Censored Text Storage
python3 RawTextStorage.py & > /dev/null
raw_storage=$(echo $!)
python3 CensoredTextStorage.py ${petitions} >> logging/InsultFilterService.log &
censored_storage=$(echo $!)

# Wait some time so both Raw and Censored Text Storage can start correctly
sleep 1

# Start nodes of Insult Filter Service
insult_filter_port=8012
insult_filter_pids=()

for ((i=0; i<$nodes; i++)); do
	python3 InsultFilterService.py "$((i + insult_filter_port))" & > /dev/null
	pid=$!
	insult_filter_pids+=("$pid")
done

# Wait some time so all Insult Filter Service can start correctly
sleep 1

# Open node Storage Publisher
python3 InsultPublisher.py & 1> /dev/null
insult_publisher=$(echo $!)

# Wait some time so Storage Publisher can start correctly
sleep 1

# Open new node Insult Storage
python3 InsultStorage.py & 1> /dev/null
insult_storage=$(echo $!)

# Wait some time so Insult Storage can start correctly
sleep 1

# Open new node EventPublisher
python3 EventPublisher.py & 1> /dev/null
event_publisher=$(echo $!)

# Wait some time so Publisher can start correctly
sleep 1

# Open new nodes Subscribers
python3 Subscriber.py 8010 & 1> /dev/null
event_subscriber1=$(echo $!)
python3 Subscriber.py 8011 & 1> /dev/null
event_subscriber2=$(echo $!)

# Wait some time so Subscribers can start correctly
sleep 1

# Start nodes of Insult Service
insult_port=8112
insult_pids=()

for ((i=0; i<$nodes; i++)); do
	python3 InsultService.py "$((i + insult_port))" & > /dev/null
	pid=$!
	insult_pids+=("$pid")
done

# Wait some time so Insult Service can start correctly
sleep 1

echo "Time with '"${nodes}"' nodes, '"${petitions}"' petitions and '"${threads}"' threads:" >> logging/InsultService.log

# Initialize a client tester with petitions and threads to use
python3 InsultClientStress.py $petitions $threads >> logging/InsultService.log

# Wait some time so all changes are processed through the system
sleep 10

echo "Time with '"${nodes}"' nodes, '"${petitions}"' petitions and '"${threads}"' threads:" >> logging/InsultFilterService.log
python3 InsultFilterClientStress.py $petitions $threads >> logging/InsultFilterService.log

wait $censored_storage

kill $name_server
kill $raw_storage
for pid in "${insult_filter_pids[@]}"; do
    kill $pid
done
kill $insult_publisher
kill $insult_storage
kill $event_publisher
kill $event_subscriber1
kill $event_subscriber2
for pid in "${insult_pids[@]}"; do
    kill $pid
done

START_LINE=$(tail -n 2 "logging/InsultFilterService.log" | head -n 1)
END_LINE=$(tail -n 1 "logging/InsultFilterService.log")

START_TIME=$(echo "$START_LINE" | awk -F': ' '{print $2}')
END_TIME=$(echo "$END_LINE" | awk -F': ' '{print $2}')

head -n -2 "logging/InsultFilterService.log" > temp_file

DURATION=$(awk "BEGIN {printf \"%.2f\", $END_TIME - $START_TIME}")
echo "Total time: $DURATION seconds" >> temp_file

mv temp_file "logging/InsultFilterService.log"
