#!/bin/bash
set -e

apt update && apt upgrade -y

apt install -y wireguard
apt install -y python3 python3-pip python3-venv

python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem -subj "/C=RU/ST=no/L=no/O=no/OU=no/CN=no"

gunicorn -w 4 -b 0.0.0.0:5000 run:app --certfile=cert.pem --keyfile=key.pem