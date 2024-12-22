from flask import Flask
from app.routes import init_routes

app = Flask(__name__)
init_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, ssl_context=('cert.pem', 'key.pem'))