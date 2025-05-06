#! /bin/bash

if [ -f "time_log" ]; then
    rm ftime_log
fi

./system_initializer.sh 1 100 4
./system_initializer.sh 2 100 4
./system_initializer.sh 3 100 4

./system_initializer.sh 1 200 4
./system_initializer.sh 2 200 4
./system_initializer.sh 3 200 4

./system_initializer.sh 1 500 4
./system_initializer.sh 2 500 4
./system_initializer.sh 3 500 4

./system_initializer.sh 1 1000 4
./system_initializer.sh 2 1000 4
./system_initializer.sh 3 1000 4

./system_initializer.sh 1 5000 4
./system_initializer.sh 2 5000 4
./system_initializer.sh 3 5000 4
