#! /bin/bash

# TODO: Check if python has virtual env
#   -> milax doesn't enable pip install redis
python3 -m venv venv
source venv/bin/activate
pip install redis

if [ -f time_log ]; then
    rm time_log
fi

./system_initializer.sh 1 500
./system_initializer.sh 2 500
./system_initializer.sh 4 500
./system_initializer.sh 8 500

./system_initializer.sh 1 800
./system_initializer.sh 2 800
./system_initializer.sh 4 800
./system_initializer.sh 8 800

./system_initializer.sh 1 1000
./system_initializer.sh 2 1000
./system_initializer.sh 4 1000
./system_initializer.sh 8 1000

./system_initializer.sh 1 1500
./system_initializer.sh 2 1500
./system_initializer.sh 4 1500
./system_initializer.sh 8 1500

./system_initializer.sh 1 2500
./system_initializer.sh 2 2500
./system_initializer.sh 4 2500
./system_initializer.sh 8 2500

./system_initializer.sh 1 4000
./system_initializer.sh 2 4000
./system_initializer.sh 4 4000
./system_initializer.sh 8 4000

./system_initializer.sh 1 5000
./system_initializer.sh 2 5000
./system_initializer.sh 4 5000
./system_initializer.sh 8 5000

./system_initializer.sh 1 10000
./system_initializer.sh 2 10000
./system_initializer.sh 4 10000
./system_initializer.sh 8 10000

./system_initializer.sh 1 15000
./system_initializer.sh 2 15000
./system_initializer.sh 4 15000
./system_initializer.sh 8 15000

./system_initializer.sh 1 20000
./system_initializer.sh 2 20000
./system_initializer.sh 4 20000
./system_initializer.sh 8 20000
