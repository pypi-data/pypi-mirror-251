# Created By: Eric Dennis
# Version: 1.0.0
# Last Updated: 1/16/2024
# Purpose: A module to fetch your's/other's IP/ information.


### -- IMPORTS -- ###

import requests
import socket
import json


### -- PUBLIC IP METHODS -- ###

def info():
    try:
        response = requests.get("https://ipinfo.io/json").json()
        return response
    except requests.RequestException as e:
        # Handle exceptions if the request to the API fails
        print(f"Error fetching IP information: {e}")
        return None

def public_ip():
    response = info()
    return str(response.get('ip'))

def public_hostname():
    response = info()
    return str(response.get('hostname'))

def public_city():
    response = info()
    return str(response.get('city'))

def public_region():
    response = info()
    return str(response.get('region'))

def public_country():
    response = info()
    return str(response.get('country'))

def public_loc():
    response = info()
    return str(response.get('loc'))

def public_organization():
    response = info()
    return str(response.get('org'))

def public_postal():
    response = info()
    return str(response.get('postal'))

def public_fulladdress():
    response = info()
    return f"{response.get('city', 'N/A')}, {response.get('region', 'N/A')}, {response.get('country', 'N/A')}, {response.get('postal', 'N/A')}"

def public_timezone():
    response = info()
    return str(response.get('timezone'))


### -- PRIVATE INFORMATION -- ###

def private_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            private_ip = s.getsockname()[0]
        return str(private_ip)
    except (socket.error, OSError) as e:
        print(f"Error fetching private IP: {e}")
        return None


### -- OTHER INFORMATION -- ###

def open_ports():
    open_ports_list = []
    ip = socket.gethostbyname(socket.gethostname())
    for port in range(65535):
        try:
            serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serv.bind((ip, port))
        except socket.error:
            open_ports_list.append(int(port))
        finally:
            serv.close()
    return open_ports_list


def ip_probe(ip_address, indent=False):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        response.raise_for_status()
        data = response.json()

        if indent:
            return json.dumps(data, indent=2)
        else:
            return json.dumps(data, indent=None)

    except requests.RequestException as e:
        print(f"Error probing IP information: {e}")
        return None
