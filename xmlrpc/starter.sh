#! /bin/bash

# Open new terminal with Name Server
#gnome-terminal --title="Name Server" -- bash -c "python3 NameServer.py" &
python3 NameServer.py & 1> /dev/null
name_server=$(echo $!)

# Wait some time so Name Server can start correctly
sleep 1

# Open new terminal with both Raw and Censored Text Storage 
#gnome-terminal --title="Raw Text Storage" -- bash -c "python3 RawTextStorage.py" &
python3 RawTextStorage.py & 1> /dev/null
raw_storage=$(echo $!)
#gnome-terminal --title="Censored Text Storage" -- bash -c "python3 CensoredTextStorage.py" &
python3 CensoredTextStorage.py & 1> /dev/null
censored_storage=$(echo $!)

# Wait some time so both Raw and Censored Text Storage can start correctly
sleep 1

# Open new terminal with 1 .. n Insult Filter
#gnome-terminal --title="Insult Filter Service 1" -- bash -c "python3 InsultFilterService.py 8012" &
python3 InsultFilterService.py 8012 & 1> /dev/null
insult_filter=$(echo $!)

# Wait some time so all Insult Filter Service can start correctly
sleep 1

# Open new terminal with Storage Publisher
#gnome-terminal --title="Insult Publisher" -- bash -c "python3 InsultPublisher.py" &
python3 InsultPublisher.py & 1> /dev/null
insult_publisher=$(echo $!)

# Wait some time so Storage Publisher can start correctly
sleep 1

# Open new terminal with Insult Storage
#gnome-terminal --title="Insult Storage" -- bash -c "python3 InsultStorage.py" &
python3 InsultStorage.py & 1> /dev/null
insult_storage=$(echo $!)

# Wait some time so Insult Storage can start correctly
sleep 1

# Open new terminal with Publisher
#gnome-terminal --title="EventPublisher" -- bash -c "python3 EventPublisher.py" &
python3 EventPublisher.py & 1> /dev/null
event_publisher=$(echo $!)

# Wait some time so Publisher can start correctly
sleep 1

# Open new terminals with Subscriber
#gnome-terminal --title="Subscriber 1" -- bash -c "python3 Subscriber.py 8010" &
python3 Subscriber.py 8010 & 1> /dev/null
event_subscriber1=$(echo $!)

#gnome-terminal --title="Subscriber 2" -- bash -c "python3 Subscriber.py 8011" &
python3 Subscriber.py 8011 & 1> /dev/null
event_subscriber2=$(echo $!)

# Wait some time so Subscribers can start correctly
sleep 1

# Open new terminal with 1 .. n Insult Service
#gnome-terminal --title="Insult Service 1" -- bash -c "python3 InsultService.py 8014" &
python3 InsultService.py 8014 &
insult_service1=$(echo $!)
#gnome-terminal --title="Insult Service 2" -- bash -c "python3 InsultService.py 8015" &
python3 InsultService.py 8015 &
insult_service2=$(echo $!)
#gnome-terminal --title="Insult Service 3" -- bash -c "python3 InsultService.py 8016" &
python3 InsultService.py 8016 &
insult_service3=$(echo $!)

# Wait some time so Insult Service can start correctly
sleep 1

# Open new terminal with client
#gnome-terminal --title="Insult Client 1" -- bash -c "python3 InsultClient.py 1> time_log" &
echo "3 node:" 1>> time_log
#start=$(date +%s)
#echo $start 1>> time_log

python3 InsultClientStress.py >> time_log
#pid1=$(echo $!)
#python3 InsultClientStress.py &
#pid2=$(echo $!)
#python3 InsultClientStress.py &
#pid3=$(echo $!)
#python3 InsultClientStress.py 

#wait $pid1
#wait $pid2
#wait $pid3

#end=$(date +%s)
#echo $end 1>> time_log
#echo "Total time: $((end - start)) seconds" 1>> time_log

sleep 10

kill $name_server
kill $raw_storage
kill $censored_storage
kill $insult_filter
kill $insult_publisher
kill $insult_storage
kill $event_publisher
kill $event_subscriber1
kill $event_subscriber2
kill $insult_service1
kill $insult_service2
kill $insult_service3

#gnome-terminal --title="Insult Filter Client 1" -- bash -c "python3 InsultFilterClient.py" &

