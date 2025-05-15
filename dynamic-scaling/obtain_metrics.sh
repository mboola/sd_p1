#! /bin/bash

python3 InsultService/client.py 1000
python3 InsultService/client.py 100 &

sleep 1

python3 InsultService/client.py 1000 &
python3 InsultService/client.py 100 &

sleep 1

python3 InsultService/client.py 100 &
python3 InsultService/client.py 1000 &

sleep 2

python3 InsultService/client.py 100
python3 InsultService/client.py 1000 &

sleep 1

python3 InsultService/client.py 1000 &
python3 InsultService/client.py 5000 &
sleep 1

python3 InsultService/client.py 1000