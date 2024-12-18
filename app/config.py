from os import getenv

# Загрузка переменных окружения
API_KEY = getenv("API_KEY")

WG_CONF = getenv("WG_CONF")
CLIENTS_DIR = getenv("CLIENTS_DIR")
WG_INTERFACE = getenv("WG_INTERFACE")

IP_RANGE_START = int(getenv("IP_RANGE_START"))
IP_RANGE_END = int(getenv("IP_RANGE_END"))
SUBNET = getenv("SUBNET")