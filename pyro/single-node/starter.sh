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
python3 launcherTests.py 800 0
python3 launcherTests.py 1000 0
python3 launcherTests.py 1500 0
python3 launcherTests.py 2500 0
python3 launcherTests.py 4000 0
python3 launcherTests.py 5000 0
python3 launcherTests.py 10000 0
python3 launcherTests.py 15000 0
python3 launcherTests.py 20000 0

# Insult filers services:
python3 launcherTests.py 500 500
python3 launcherTests.py 800 800
python3 launcherTests.py 1000 1000
python3 launcherTests.py 1500 1500
python3 launcherTests.py 2500 2500
python3 launcherTests.py 4000 4000
python3 launcherTests.py 5000 5000
python3 launcherTests.py 10000 10000
python3 launcherTests.py 15000 15000
python3 launcherTests.py 20000 20000