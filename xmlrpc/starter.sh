#! /bin/bash

# Open new terminal with Name Server
gnome-terminal -- bash -c "python3 NameServer.py" &

# Wait some time so Name Server can start correctly
sleep 1

# Open new terminal with both Raw and Censored Text Storage 
gnome-terminal -- bash -c "python3 RawTextStorage.py" &
gnome-terminal -- bash -c "python3 CensoredTextStorage.py" &

# Wait some time so both Raw and Censored Text Storage can start correctly
sleep 1

# Open new terminal with 1 .. n Insult Filter
gnome-terminal -- bash -c "python3 InsultFilterService.py 8010" &

# Wait some time so all Insult Filter Service can start correctly
sleep 1

# Open new terminal with Storage Publisher
#gnome-terminal -- bash -c "python3 StoragePublisher.py" &

# Open new terminal with Insult Storage
#gnome-terminal -- bash -c "python3 InsultStorage.py" &

# Open new terminal with Publisher
#gnome-terminal -- bash -c "python3 Publisher.py" &

# Wait some time so Publisher can start correctly
#sleep 1

# Open new terminals with Subscriber
#gnome-terminal -- bash -c "python3 Subscriber.py 8011" &
#gnome-terminal -- bash -c "python3 Subscriber.py 8012" &

# Open new terminal with 1 .. n Insult Service
#gnome-terminal -- bash -c "python3 InsultService.py 8013" &

# Wait some time so Insult Service can start correctly
#sleep 1

# Open new terminal with client
#gnome-terminal -- bash -c "python3 InsultClient.py" &
