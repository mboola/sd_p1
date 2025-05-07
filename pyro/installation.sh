#!/bin/bash

set -e

sudo apt update
sudo apt upgrade -y

echo "Instalando Python3 y pip..."
sudo apt install -y python3 python3-pip

echo "Instalando Redis..."
sudo apt install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server

echo "Todo listo."
