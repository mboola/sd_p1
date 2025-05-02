#! /bin/bash
#
# Shows communication producer-consumer using redis with docker

# TODO : check if docker exists and stop, delete it or whatever

# Starts redis server
sudo docker run --name InsultRedis -d -p 6379:6379 redis

# Open new terminal with producer
gnome-terminal --title="Insult Client" -- bash -c "python3 InsultClient.py" &

# Open new terminal with Subscriber 1
gnome-terminal --title="Subscriber 1" -- bash -c "python3 Subscriber.py" &

# Open new terminal with Subscriber 2
gnome-terminal --title="Subscriber 2" -- bash -c "python3 Subscriber.py" &

# Open new terminal with Event Publisher
gnome-terminal --title="Event Publisher" -- bash -c "python3 EventPublisher.py" &

# Open new terminal with Insult Filter Client
gnome-terminal --title="Insult Client" -- bash -c "python3 InsultFilterClient.py" &

# Open new terminal with Insult Filter Service
gnome-terminal --title="Insult Filter Service 1" -- bash -c "python3 InsultFilterService.py" &
gnome-terminal --title="Insult Filter Service 2" -- bash -c "python3 InsultFilterService.py" &

echo -e "\e[31mWaiting 20 seconds and then closing redis.\e[0m"
sleep 20
echo -e "\e[31mClosing redis.\e[0m"

sudo docker stop InsultRedis
sudo docker remove InsultRedis
