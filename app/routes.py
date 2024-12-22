from flask import request, jsonify
from app.auth import authenticate_request
from app.wg import WireGuard

wg = WireGuard()

def init_routes(app):
    @app.route("/create_client", methods=["POST"])
    def create_client():
        if not authenticate_request():
            return jsonify({"error": "Unauthorized"}), 401

        data = request.json
        subscription_id = data.get("subscription_id")
        if not subscription_id:
            return jsonify({"error": "Subscription ID is required"}), 400


        client_config = wg.create_client(subscription_id)

        return jsonify({"message": "Client created successfully", "client_config": client_config}), 201

    @app.route("/delete_client", methods=["POST"])
    def delete_client():
        if not authenticate_request():
            return jsonify({"error": "Unauthorized"}), 401

        data = request.json
        subscription_id = data.get("subscription_id")
        if not subscription_id:
            return jsonify({"error": "Subscription ID is required"}), 400

        wg.delete_client(subscription_id)

        return jsonify({"message": "Client deleted successfully"}), 200
    
    @app.route("/delete_client", methods=["POST"])
    def get_client():
        if not authenticate_request():
            return jsonify({"error": "Unauthorized"}), 401

        data = request.json
        subscription_id = data.get("subscription_id")
        if not subscription_id:
            return jsonify({"error": "Subscription ID is required"}), 400

        client_config = wg.get_client(subscription_id)

        return jsonify({"message": "Client getted successfully", "client_config": client_config}), 200