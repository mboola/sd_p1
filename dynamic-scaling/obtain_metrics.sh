#! /bin/bash

client=$1

python3 ${client} 1000
python3 ${client} 100 &

sleep 1

python3 ${client} 1000 &
python3 ${client} 100 &

sleep 1

python3 ${client} 100 &
python3 ${client} 1000 &

sleep 2

python3 ${client} 100
python3 ${client} 1000 &

sleep 1

python3 ${client} 1000 &
python3 ${client} 5000 &
sleep 1

python3 ${client} 1000