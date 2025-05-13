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

./system_initializer.sh 1 1000 4
./system_initializer.sh 2 1000 4
./system_initializer.sh 3 1000 4
./system_initializer.sh 4 1000 4

./system_initializer.sh 1 5000 4
./system_initializer.sh 2 5000 4
./system_initializer.sh 3 5000 4
./system_initializer.sh 4 5000 4

./system_initializer.sh 1 10000 4
./system_initializer.sh 2 10000 4
./system_initializer.sh 3 10000 4
./system_initializer.sh 4 10000 4

./system_initializer.sh 1 20000 4
./system_initializer.sh 2 20000 4
./system_initializer.sh 3 20000 4
./system_initializer.sh 4 20000 4
