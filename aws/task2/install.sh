#!/bin/bash

set -e

ARCH=$(uname -m)

if [ "$ARCH" = "x86_64" ]; then
    URL="https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
elif [ "$ARCH" = "aarch64" ]; then
    URL="https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip"
else
    echo "Arquitectura no soportada: $ARCH"
    exit 1
fi

echo "Descargando AWS CLI para arquitectura $ARCH..."
curl "$URL" -o "awscliv2.zip"

echo "Descomprimiendo..."
unzip -o awscliv2.zip

echo "Instalando AWS CLI..."
sudo ./aws/install --update

clear

set -e

echo "Actualizando el sistema..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip unzip

echo "Instalando boto3 y dependencias..."
pip3 install --upgrade pip
pip3 install boto3

echo "Configurando AWS CLI (ejecuta esto manualmente si no tienes variables de entorno AWS):"
echo "  aws configure"

clear

echo "Instalación completa."
echo "Listo. Ya puedes ejecutar launcher.py"

