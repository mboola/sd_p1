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

set -e

$SUDO apt update -y
$SUDO apt upgrade -y

clear

echo "> Instalando Python3 y pip..."
if ! command -v python3 >/dev/null || ! command -v pip3 >/dev/null; then
  $SUDO apt-get install -y python3 python3-pip python3-venv
else
  echo "Python3 y pip ya están instalados."
fi

clear

echo "> Instalando Docker..."
if ! command -v docker >/dev/null; then
  $SUDO apt-get install -y apt-transport-https ca-certificates curl software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | $SUDO gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
    https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
    $SUDO tee /etc/apt/sources.list.d/docker.list > /dev/null
  $SUDO apt-get update -y
  $SUDO apt-get install -y docker-ce docker-ce-cli containerd.io
  $SUDO systemctl enable docker
  $SUDO systemctl start docker
else
  echo "Docker ya está instalado."
fi

clear

echo "> Instalando el contenedor Redis..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

REQ_FILE="$SCRIPT_DIR/../requirements.txt"
if [ ! -f "$REQ_FILE" ]; then
  echo "No se encontró $REQ_FILE"
  exit 1
fi

$SUDO pip3 install -r "$SCRIPT_DIR/../requirements.txt" --break-system-packages
if ! $SUDO docker container inspect redis-container >/dev/null 2>&1; then
  $SUDO docker pull redis:latest
  $SUDO docker run -d --name redis-container -p 6379:6379 redis:latest
else
  echo "El contenedor 'redis-container' ya existe."
fi

clear

echo "> Corriendo contenedor RabbitMQ..."
if ! $SUDO docker container inspect rabbitmq >/dev/null 2>&1; then #$SUDO docker ps -a | grep rabbitmq; then
  $SUDO docker pull rabbitmq:management
  $SUDO docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
  echo "> Esperando a que RabbitMQ inicie..."
  sleep 10
else
  echo "El contenedor 'rabbitmq' ya existe."
  $SUDO docker start rabbitmq >/dev/null || true
fi

clear

echo "> Verificando si RabbitMQ está corriendo..."
if $SUDO docker ps --filter "name=rabbitmq" --filter "status=running" | grep -q rabbitmq; then
  echo "> Creando usuario 'ar' si no existe..."
  if ! $SUDO docker exec rabbitmq rabbitmqctl list_users | grep -q "^ar"; then
    $SUDO docker exec rabbitmq rabbitmqctl add_user ar sar
    $SUDO docker exec rabbitmq rabbitmqctl set_permissions -p / ar ".*" ".*" ".*"
    echo "Usuario 'ar' creado y permisos asignados."
  else
    echo "El usuario 'ar' ya existe."
  fi
else
  echo "Error: El contenedor 'rabbitmq' no está corriendo."
  exit 1
fi

clear

echo "Todo listo:"
echo "OK.. RabbitMQ está corriendo en el contenedor 'rabbitmq'."
echo "OK.. Redis está corriendo en el contenedor 'redis-container'."
echo "OK.. RabbitMQ está disponible en el puerto 5672."
echo "OK.. Redis está disponible en el puerto 6379."
echo "OK.. RabbitMQ Management UI está disponible en el puerto 15672."
echo "OK.. RabbitMQ Management UI:"
echo "- URL: http://localhost:15672"
echo "- Usuario: ar"
echo "- Contraseña: sar"
echo "OK.. Redis:"
echo "- URL: redis://localhost:6379"
