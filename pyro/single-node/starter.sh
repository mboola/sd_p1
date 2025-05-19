#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Este script debe ejecutarse como root o con sudo."
  exit 1
fi

if [ "$(id -u)" -eq 0 ]; then
  SUDO=""
else
  SUDO="sudo"
fi

$SUDO bash ../installation.sh

if [ $? -ne 0 ]; then
  echo "Fallo al ejecutar installation.sh abortando..."
  exit 1
fi

# Insult services:
python3 launcherTests.py 500 0
sudo docker stop redis-container

sudo docker rm redis-container

sudo docker pull redis:latest

sudo docker run -d --name redis-container -p 6379:6379 redis:latest
python3 launcherTests.py 800 0
sudo docker stop redis-container

sudo docker rm redis-container

sudo docker pull redis:latest

sudo docker run -d --name redis-container -p 6379:6379 redis:latest
python3 launcherTests.py 1000 0
sudo docker stop redis-container

sudo docker rm redis-container

sudo docker pull redis:latest

sudo docker run -d --name redis-container -p 6379:6379 redis:latest
python3 launcherTests.py 1500 0
sudo docker stop redis-container

sudo docker rm redis-container

sudo docker pull redis:latest

sudo docker run -d --name redis-container -p 6379:6379 redis:latest
python3 launcherTests.py 2500 0
sudo docker stop redis-container

sudo docker rm redis-container

sudo docker pull redis:latest

sudo docker run -d --name redis-container -p 6379:6379 redis:latest
python3 launcherTests.py 4000 0
sudo docker stop redis-container

sudo docker rm redis-container

sudo docker pull redis:latest

sudo docker run -d --name redis-container -p 6379:6379 redis:latest
python3 launcherTests.py 5000 0
sudo docker stop redis-container

sudo docker rm redis-container

sudo docker pull redis:latest

sudo docker run -d --name redis-container -p 6379:6379 redis:latest
python3 launcherTests.py 10000 0
sudo docker stop redis-container

sudo docker rm redis-container

sudo docker pull redis:latest

sudo docker run -d --name redis-container -p 6379:6379 redis:latest
python3 launcherTests.py 15000 0
sudo docker stop redis-container

sudo docker rm redis-container

sudo docker pull redis:latest

sudo docker run -d --name redis-container -p 6379:6379 redis:latest
python3 launcherTests.py 20000 0
sudo docker stop redis-container

sudo docker rm redis-container

sudo docker pull redis:latest

sudo docker run -d --name redis-container -p 6379:6379 redis:latest

# Insult filers services:
python3 launcherTests.py 500 500
sudo docker stop redis-container

sudo docker rm redis-container

sudo docker pull redis:latest

sudo docker run -d --name redis-container -p 6379:6379 redis:latest
python3 launcherTests.py 800 800
sudo docker stop redis-container

sudo docker rm redis-container

sudo docker pull redis:latest

sudo docker run -d --name redis-container -p 6379:6379 redis:latest
python3 launcherTests.py 1000 1000
sudo docker stop redis-container

sudo docker rm redis-container

sudo docker pull redis:latest

sudo docker run -d --name redis-container -p 6379:6379 redis:latest
python3 launcherTests.py 1500 1500
sudo docker stop redis-container

sudo docker rm redis-container

sudo docker pull redis:latest

sudo docker run -d --name redis-container -p 6379:6379 redis:latest
python3 launcherTests.py 2500 2500
sudo docker stop redis-container

sudo docker rm redis-container

sudo docker pull redis:latest

sudo docker run -d --name redis-container -p 6379:6379 redis:latest
python3 launcherTests.py 4000 4000
sudo docker stop redis-container

sudo docker rm redis-container

sudo docker pull redis:latest

sudo docker run -d --name redis-container -p 6379:6379 redis:latest
python3 launcherTests.py 5000 5000
sudo docker stop redis-container

sudo docker rm redis-container

sudo docker pull redis:latest

sudo docker run -d --name redis-container -p 6379:6379 redis:latest
python3 launcherTests.py 10000 10000
sudo docker stop redis-container

sudo docker rm redis-container

sudo docker pull redis:latest

sudo docker run -d --name redis-container -p 6379:6379 redis:latest
python3 launcherTests.py 15000 15000
sudo docker stop redis-container

sudo docker rm redis-container

sudo docker pull redis:latest

sudo docker run -d --name redis-container -p 6379:6379 redis:latest
python3 launcherTests.py 20000 20000
sudo docker stop redis-container

sudo docker rm redis-container