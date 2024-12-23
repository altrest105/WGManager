from os import getenv
from dotenv import load_dotenv

load_dotenv()

# API
API_KEY = getenv("API_KEY")

# WireGuard
WG_CONF = getenv("WG_CONF")
CLIENTS_DIR = getenv("CLIENTS_DIR")
WG_INTERFACE = getenv("WG_INTERFACE")
LISTEN_PORT = int(getenv("LISTEN_PORT"))