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

#python3 launcher.py <number_insult_services> <number_filter_services> <number_insults> <number_texts_to_filter>

# Insult services:
python3 launcher.py 1 1 500 0
python3 launcher.py 1 1 800 0
python3 launcher.py 1 1 1000 0
python3 launcher.py 1 1 1500 0
python3 launcher.py 1 1 2500 0
python3 launcher.py 1 1 4000 0
python3 launcher.py 1 1 5000 0
python3 launcher.py 1 1 10000 0
python3 launcher.py 1 1 15000 0
python3 launcher.py 1 1 20000 0

python3 launcher.py 2 1 500 0
python3 launcher.py 2 1 800 0
python3 launcher.py 2 1 1000 0
python3 launcher.py 2 1 1500 0
python3 launcher.py 2 1 2500 0
python3 launcher.py 2 1 4000 0
python3 launcher.py 2 1 5000 0
python3 launcher.py 2 1 10000 0
python3 launcher.py 2 1 15000 0
python3 launcher.py 2 1 20000 0

python3 launcher.py 4 1 500 0
python3 launcher.py 4 1 800 0
python3 launcher.py 4 1 1000 0
python3 launcher.py 4 1 1500 0
python3 launcher.py 4 1 2500 0
python3 launcher.py 4 1 4000 0
python3 launcher.py 4 1 5000 0
python3 launcher.py 4 1 10000 0
python3 launcher.py 4 1 15000 0
python3 launcher.py 4 1 20000 0

python3 launcher.py 8 1 500 0
python3 launcher.py 8 1 800 0
python3 launcher.py 8 1 1000 0
python3 launcher.py 8 1 1500 0
python3 launcher.py 8 1 2500 0
python3 launcher.py 8 1 4000 0
python3 launcher.py 8 1 5000 0
python3 launcher.py 8 1 10000 0
python3 launcher.py 8 1 15000 0
python3 launcher.py 8 1 20000 0

# Insult filers services:
python3 launcher.py 1 1 500 500
python3 launcher.py 1 1 800 800
python3 launcher.py 1 1 1000 1000
python3 launcher.py 1 1 1500 1500
python3 launcher.py 1 1 2500 2500
python3 launcher.py 1 1 4000 4000
python3 launcher.py 1 1 5000 5000
python3 launcher.py 1 1 10000 10000
python3 launcher.py 1 1 15000 15000
python3 launcher.py 1 1 20000 20000

python3 launcher.py 2 2 500 500
python3 launcher.py 2 2 800 800
python3 launcher.py 2 2 1000 1000
python3 launcher.py 2 2 1500 1500
python3 launcher.py 2 2 2500 2500
python3 launcher.py 2 2 4000 4000
python3 launcher.py 2 2 5000 5000
python3 launcher.py 2 2 10000 10000
python3 launcher.py 2 2 15000 15000
python3 launcher.py 2 2 20000 20000

python3 launcher.py 4 4 500 500
python3 launcher.py 4 4 800 800
python3 launcher.py 4 4 1000 1000
python3 launcher.py 4 4 1500 1500
python3 launcher.py 4 4 2500 2500
python3 launcher.py 4 4 4000 4000
python3 launcher.py 4 4 5000 5000
python3 launcher.py 4 4 10000 10000
python3 launcher.py 4 4 15000 15000
python3 launcher.py 4 4 20000 20000

python3 launcher.py 8 8 500 500
python3 launcher.py 8 8 800 800
python3 launcher.py 8 8 1000 1000
python3 launcher.py 8 8 1500 1500
python3 launcher.py 8 8 2500 2500
python3 launcher.py 8 8 4000 4000
python3 launcher.py 8 8 5000 5000
python3 launcher.py 8 8 10000 10000
python3 launcher.py 8 8 15000 15000
python3 launcher.py 8 8 20000 20000