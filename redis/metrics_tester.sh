#! /bin/bash

# TODO: Check if python has virtual env
#   -> milax doesn't enable pip install redis
python3 -m venv venv
source venv/bin/activate
pip install redis

if [ -f time_log ]; then
    rm time_log
fi


#./system_initializer.sh 1 100
#./system_initializer.sh 2 100
#./system_initializer.sh 3 100
#./system_initializer.sh 4 100

./system_initializer.sh 1 200
#./system_initializer.sh 2 200
#./system_initializer.sh 3 200
#./system_initializer.sh 4 200

#./system_initializer.sh 1 500
#./system_initializer.sh 2 500
#./system_initializer.sh 3 500
#./system_initializer.sh 4 500

#./system_initializer.sh 1 1000
#./system_initializer.sh 2 1000
#./system_initializer.sh 3 1000
#./system_initializer.sh 4 1000

#./system_initializer.sh 1 5000
#./system_initializer.sh 2 5000
#./system_initializer.sh 3 5000
#./system_initializer.sh 4 5000
