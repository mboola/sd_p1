#! /bin/bash

if [ -f logging/InsultFilterService.log ]; then
    rm logging/InsultFilterService.log
fi

if [ -f logging/InsultService.log ]; then
    rm logging/InsultService.log
fi

./system_initializer.sh 1 500 4
./system_initializer.sh 2 500 4
./system_initializer.sh 3 500 4
./system_initializer.sh 4 500 4

./system_initializer.sh 1 800 4
./system_initializer.sh 2 800 4
./system_initializer.sh 3 800 4
./system_initializer.sh 4 800 4

./system_initializer.sh 1 1000 4
./system_initializer.sh 2 1000 4
./system_initializer.sh 3 1000 4
./system_initializer.sh 4 1000 4

./system_initializer.sh 1 1500 4
./system_initializer.sh 2 1500 4
./system_initializer.sh 3 1500 4
./system_initializer.sh 4 1500 4

./system_initializer.sh 1 2500 4
./system_initializer.sh 2 2500 4
./system_initializer.sh 3 2500 4
./system_initializer.sh 4 2500 4

./system_initializer.sh 1 4000 4
./system_initializer.sh 2 4000 4
./system_initializer.sh 3 4000 4
./system_initializer.sh 4 4000 4

./system_initializer.sh 1 5000 4
./system_initializer.sh 2 5000 4
./system_initializer.sh 3 5000 4
./system_initializer.sh 4 5000 4

./system_initializer.sh 1 10000 4
./system_initializer.sh 2 10000 4
./system_initializer.sh 3 10000 4
./system_initializer.sh 4 10000 4

./system_initializer.sh 1 15000 4
./system_initializer.sh 2 15000 4
./system_initializer.sh 3 15000 4
./system_initializer.sh 4 15000 4

./system_initializer.sh 1 20000 4
./system_initializer.sh 2 20000 4
./system_initializer.sh 3 20000 4
./system_initializer.sh 4 20000 4
