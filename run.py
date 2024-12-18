from flask import Flask
from app.routes import init_routes
from os import getenv

# Загрузка переменных окружения
API_KEY = getenv("API_KEYS")

WG_CONF = getenv("WG_CONF")
CLIENTS_DIR = getenv("CLIENTS_DIR")
WG_INTERFACE = getenv("WG_INTERFACE")

IP_RANGE_START = int(getenv("IP_RANGE_START"))
IP_RANGE_END = int(getenv("IP_RANGE_END"))
SUBNET = getenv("SUBNET")

# Создание экземпляра Flask
app = Flask(__name__)
init_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)