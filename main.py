import subprocess
import time
import os
import json
import socket
import requests


def is_nmap_installed():
    return os.path.exists("c:\\Program Files (x86)\\Nmap\\nmap.exe")

def install_nmap():
    try:
        subprocess.run(["pip", "install", "nmap"])
    except subprocess.CalledProcessError as e:
        print("An error occurred during the installation of nmap:", e)

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        public_ip = data['ip']
        return public_ip
    except Exception as e:
        print("An error occurred while retrieving public IP:", e)
        return None

def save_public_ip_to_json(public_ip):
    if public_ip is not None:
        public_ip_data = {"public_ip": public_ip}
        with open("public_ip.json", 'w') as json_file:
            json.dump(public_ip_data, json_file, indent=3)

    else:
        print("Failed to retrieve public IP. JSON file not saved.")

if __name__ == "__main__":
    public_ip = get_public_ip()
    save_public_ip_to_json(public_ip)

def get_local_ip_address():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]

def local_scan():
    local_ip = get_local_ip_address()
    nmap_cmd = ["nmap", "-sV", local_ip]
    try:
        scan_output = subprocess.run(nmap_cmd, capture_output=True, text=True, check=True).stdout
        open_ports = []
        for line in scan_output.splitlines():
            if "open" in line and "tcp" in line:
                port_info = line.split()
                port = port_info[0]
                service = port_info[2]
                open_ports.append({"port": port, "service": service})

        with open("local_scan.json", 'w') as json_file:
            json.dump(open_ports, json_file, indent=3)

        return open_ports
    except subprocess.CalledProcessError as e:
        print("Error occurred during local scan:", e)
        return []

def LAN_scan():
    LAN_ip = "192.168.1.1"
    nmap_cmd = ['nmap', LAN_ip, '-sV']
    try:
        scan_output = subprocess.run(nmap_cmd, capture_output=True, text=True, check=True).stdout
        open_ports = []
        for line in scan_output.splitlines():
            if "open" in line:
                port_info = line.split()
                port = port_info[0]
                service = port_info[2]
                open_ports.append({"port": port, "service": service})

        with open("LAN.json", 'w') as json_file:
            json.dump(open_ports, json_file, indent=3)

        return open_ports
    except subprocess.CalledProcessError as e:
        print("Error occurred during LAN scan:", e)
        return []

def send_results_to_server(filename, url):
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)

        response = requests.post(url, json=data)

        if response.status_code == 200:
            print("Scan results sent successfully.")
        else:
            print("Failed to send scan results. Status code:", response.status_code)

    except Exception as e:
        print("An error occurred while sending scan results:", e)

if __name__ == "__main__":
    if not is_nmap_installed():
        install_nmap()

    local_ip_address = get_local_ip_address()
    print("Local IP Address:", local_ip_address)

    public_ip = get_public_ip()
    save_public_ip_to_json(public_ip)
    print("Public IP saved to public_ip.json")

    localhost_res = local_scan()
    print("Localhost scan resul t:", localhost_res)

    LAN_res = LAN_scan()
    print("LAN scan:", LAN_res)

    server_url = "http://localhost:8000/"

    send_results_to_server("local_scan.json", server_url)
    send_results_to_server("LAN.json", server_url)

