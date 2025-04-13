#! /bin/bash

# Open new terminal with Name Server
gnome-terminal --title="Name Server" -- bash -c "python3 NameServer.py" &

# Wait some time so Name Server can start correctly
sleep 1

# Open new terminal with both Raw and Censored Text Storage 
gnome-terminal --title="Raw Text Storage" -- bash -c "python3 RawTextStorage.py" &
gnome-terminal --title="Censored Text Storage" -- bash -c "python3 CensoredTextStorage.py" &

# Wait some time so both Raw and Censored Text Storage can start correctly
sleep 1

# Open new terminal with 1 .. n Insult Filter
gnome-terminal --title="Insult Filter Service 1" -- bash -c "python3 InsultFilterService.py 8010" &

# Wait some time so all Insult Filter Service can start correctly
sleep 1

# Open new terminal with Storage Publisher
gnome-terminal --title="Insult Publisher" -- bash -c "python3 InsultPublisher.py" &

# Wait some time so Storage Publisher can start correctly
sleep 1

# Open new terminal with Insult Storage
gnome-terminal --title="Insult Storage" -- bash -c "python3 InsultStorage.py" &

# Wait some time so Insult Storage can start correctly
sleep 1

# Open new terminal with Publisher
gnome-terminal --title="EventPublisher" -- bash -c "python3 EventPublisher.py" &

# Wait some time so Publisher can start correctly
sleep 1

# Open new terminals with Subscriber
gnome-terminal --title="Subscriber 1" -- bash -c "python3 Subscriber.py 8011" &
gnome-terminal --title="Subscriber 2" -- bash -c "python3 Subscriber.py 8012" &

# Open new terminal with 1 .. n Insult Service
gnome-terminal --title="Insult Service 1" -- bash -c "python3 InsultService.py 8013" &

# Wait some time so Insult Service can start correctly
sleep 1

# Open new terminal with client
gnome-terminal --title="Insult Client 1" -- bash -c "python3 InsultClient.py" &
