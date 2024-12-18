import subprocess
from run import WG_CONF, IP_RANGE_START, IP_RANGE_END, SUBNET

def generate_keys():
    private_key = subprocess.check_output("wg genkey", shell=True).decode().strip()
    public_key = subprocess.check_output(f"echo {private_key} | wg pubkey", shell=True).decode().strip()
    return private_key, public_key

def get_server_ip():
    try:
        result = subprocess.run(["hostname", "-I"], capture_output=True, text=True, check=True)
        server_ip = result.stdout.strip().split()[0]
        return server_ip
    except subprocess.CalledProcessError as e:
        return str(e)

def get_free_ip():
    used_ips = set()
    with open(WG_CONF, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("AllowedIPs"):
                ip = line.split("=")[1].strip().split("/")[0]
                used_ips.add(ip)
    
    for i in range(IP_RANGE_START, IP_RANGE_END + 1):
        ip = f"{SUBNET}.{i}"
        if ip not in used_ips:
            return ip
    return None
