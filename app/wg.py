import os
import re
import subprocess
from app.config import WG_CONF, CLIENTS_DIR, WG_INTERFACE, LISTEN_PORT


class WireGuard:
    def __init__(self):
        self.wg_conf = WG_CONF
        self.clients_dir = CLIENTS_DIR
        self.interface = WG_INTERFACE
        self.listen_port = LISTEN_PORT
        self.server_ip = self.get_server_ip()
        res = subprocess.run(["sysctl", "net.ipv4.ip_forward"], capture_output=True, text=True, check=True)
        if "net.ipv4.ip_forward = 0" in res.stdout:
            subprocess.run(["sysctl", "-w", "net.ipv4.ip_forward=1"], check=True)
            subprocess.run(["sysctl", "-p"], check=True)

    def generate_keys(self):
        private_key = subprocess.check_output("wg genkey", shell=True).decode().strip()
        public_key = subprocess.check_output(f"echo {private_key} | wg pubkey", shell=True).decode().strip()
        return private_key, public_key

    def get_server_ip(self):
        result = subprocess.run(["hostname", "-I"], capture_output=True, text=True, check=True)
        server_ip = result.stdout.strip().split()[0]
        return server_ip

    def get_free_ip(self):
        used_ips = set()
        with open(self.wg_conf, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("AllowedIPs"):
                    ip = line.split("=")[1].strip().split("/")[0]
                    used_ips.add(ip)
        
        for i in range(2, 255):
            ip = f"10.8.0.{i}"
            if ip not in used_ips:
                return ip
        return None

    def get_interface(self):
        result = subprocess.run(["ip", "route"], capture_output=True, text=True, check=True)
        for line in result.stdout.strip().split("\n"):
            if line.startswith("default"):
                return line.split()[4]
    
    def check_wg(self):
        res = subprocess.run(["systemctl", "is-active", f"wg-quick@{self.interface}"], capture_output=True, text=True)
        if "inactive" in res.stdout or "failed" in res.stdout:
            subprocess.run(["systemctl", "start", f"wg-quick@{self.interface}"], check=True)

        res = subprocess.run(["systemctl", "is-enabled", f"wg-quick@{self.interface}"], capture_output=True, text=True)
        if "disabled" in res.stdout:
            subprocess.run(["systemctl", "enable", f"wg-quick@{self.interface}"], check=True)

    def create_server_config(self):
        private_key, public_key = self.generate_keys()
        ethernet_interface = self.get_interface()

        wg_conf = f"""[Interface]
PrivateKey = {private_key}
#PublicKey = {public_key}
Address = 10.8.0.1/24
ListenPort = {self.listen_port}
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o {ethernet_interface} -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o {ethernet_interface} -j MASQUERADE
"""
        with open(f"/etc/wireguard/{self.interface}.conf", "w") as f:
            f.write(wg_conf)

    def create_client(self, subscription_id):
        if not(os.path.exists(f"/etc/wireguard/{self.interface}.conf") and os.path.getsize(f"/etc/wireguard/{self.interface}.conf") > 0):
            self.create_server_config()
            self.check_wg()
        if not(os.path.exists(self.clients_dir)):
            os.makedirs(self.clients_dir)
        
        private_key, public_key = self.generate_keys()
        client_ip = self.get_free_ip()

        with open(f"/etc/wireguard/{self.interface}.conf", "r") as f:
            server_public_key = re.search(r"#PublicKey = (.{44})", f.read()).group(1)

        client_config = f"""[Interface]
PrivateKey = {private_key}
Address = {client_ip}/32
DNS = 8.8.8.8

[Peer]
PublicKey = {server_public_key}
Endpoint = {self.server_ip}:{self.listen_port}
AllowedIPs = 0.0.0.0/0"""

        client_file_path = os.path.join(self.clients_dir, f"{subscription_id}.conf")
        with open(client_file_path, "w") as f:
            f.write(client_config)

        with open(self.wg_conf, "a") as f:
            f.write(f"""
[Peer]
#subscription_id = {subscription_id}
#PrivateKey = {private_key}
PublicKey = {public_key}
AllowedIPs = {client_ip}/32
""")

        subprocess.run(f"wg set {self.interface} peer {public_key} allowed-ips {client_ip}/32", shell=True, check=True)

        return client_config

    # def delete_client(self, subscription_id):
    #     client_file_path = os.path.join(self.clients_dir, f"{subscription_id}.conf")
    #     if not os.path.exists(client_file_path):
    #         return "Client configuration file not found"

    #     with open(client_file_path, "r") as f:
    #         lines = f.readlines()
    #     client_public_key = None
    #     for line in lines:
    #         if line.startswith("PublicKey = "):
    #             client_public_key = line.split(" = ")[1].strip()
    #             break

    #     if not client_public_key:
    #         return "Client public key not found in configuration file"

    #     with open(self.wg_conf, "r") as f:
    #         lines = f.readlines()
    #     with open(self.wg_conf, "w") as f:
    #         skip = False
    #         for line in lines:
    #             if line.startswith("[Peer]") and f"PublicKey = {client_public_key}" in lines[lines.index(line)+1]:
    #                 skip = True
    #             elif skip and line.strip() == "":
    #                 skip = False
    #             elif not skip:
    #                 f.write(line)

    #     subprocess.run(f"wg set {self.interface} peer {client_public_key} remove", shell=True, check=True)

    #     os.remove(client_file_path)

    #     # Перезапуск WireGuard через systemctl
    #     result = subprocess.run(f"sudo systemctl restart wg-quick@{self.interface}", shell=True, capture_output=True, text=True)
    #     if result.returncode != 0:
    #         return f"Failed to restart WireGuard: {result.stderr}"

    #     return None