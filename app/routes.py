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
            return jsonify({"error": "Client name is required"}), 400


        client_config = wg.create_client(subscription_id)

        return jsonify({"message": "Client created successfully", "client_config": client_config}), 201

    # @app.route("/delete_client", methods=["DELETE"])
    # def delete_client():
    #     if not authenticate_request():
    #         return jsonify({"error": "Unauthorized"}), 401

    #     data = request.json
    #     subscription_id = data.get("subscription_id")
    #     if not subscription_id:
    #         return jsonify({"error": "Subscription ID is required"}), 400

    #     client_file_path = os.path.join(CLIENTS_DIR, f"{subscription_id}.conf")
    #     if not os.path.exists(client_file_path):
    #         return jsonify({"error": "Client configuration file not found"}), 404

    #     with open(client_file_path, "r") as f:
    #         lines = f.readlines()
    #     client_public_key = None
    #     for line in lines:
    #         if line.startswith("PublicKey = "):
    #             client_public_key = line.split(" = ")[1].strip()
    #             break

    #     if not client_public_key:
    #         return jsonify({"error": "Client public key not found in configuration file"}), 500

    #     with open(WG_CONF, "r") as f:
    #         lines = f.readlines()
    #     with open(WG_CONF, "w") as f:
    #         skip = False
    #         for line in lines:
    #             if line.startswith("[Peer]") and f"PublicKey = {client_public_key}" in lines[lines.index(line)+1]:
    #                 skip = True
    #             elif skip and line.strip() == "":
    #                 skip = False
    #             elif not skip:
    #                 f.write(line)

    #     subprocess.run(f"wg set {WG_INTERFACE} peer {client_public_key} remove", shell=True, check=True)

    #     os.remove(client_file_path)

    #     return jsonify({"message": "Client deleted successfully"}), 200