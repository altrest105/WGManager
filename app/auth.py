from flask import request
from run import API_KEY

def authenticate_request():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return False
    api_key = auth_header.split("Bearer ")[1]
    return api_key == API_KEY