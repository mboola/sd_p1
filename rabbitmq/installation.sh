#!/bin/bash

set -e

sudo apt update
sudo apt upgrade -y

echo "Instalando Python3 y pip..."
sudo apt install -y python3 python3-pip

echo "Instalando Docker..."
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker "$USER"

echo "Instalando Redis..."
sudo apt install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server

echo "Descargando imagen de RabbitMQ..."
sudo docker pull rabbitmq:management

echo "Corriendo contenedor RabbitMQ..."
sudo docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management

echo "Esperando a que RabbitMQ inicie..."
sleep 10

echo "Creando usuario 'ar' con contraseña 'sar'..."
sudo docker exec -it rabbitmq rabbitmqctl add_user ar sar

echo "Asignando permisos al usuario 'ar'..."
sudo docker exec -it rabbitmq rabbitmqctl set_permissions -p / ar ".*" ".*" ".*"

echo "Todo listo."
echo "- Interfaz web en: http://localhost:15672 (usuario: ar, contraseña: sar)"
