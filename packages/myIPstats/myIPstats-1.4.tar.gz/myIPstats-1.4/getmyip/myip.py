# Created By: Eric Dennis
# Version: 1.0.0
# Last Updated: 1/16/2024
# Purpose: A module to fetch your's/other's IP/ information.


### -- IMPORTS -- ###

import json
import socket
import requests


### -- MAIN CLASS -- ###

class myIPstats:

    @classmethod
    def fetch_ip_info(cls):
        try:
            response = requests.get("https://ipinfo.io/json").json()
            return response
        except requests.RequestException as e:
            # Handle exceptions if the request to the API fails
            print(f"Error fetching IP information: {e}")
            return None


    ### -- PUBLIC IP METHODS -- ###
        
    @classmethod
    def public_ip(cls):
        response = cls.fetch_ip_info()
        return str(response.get('ip'))

    @classmethod
    def public_hostname(cls):
        response = cls.fetch_ip_info()
        return str(response.get('hostname'))

    @classmethod
    def public_city(cls):
        response = cls.fetch_ip_info()
        return str(response.get('city'))

    @classmethod
    def public_region(cls):
        response = cls.fetch_ip_info()
        return str(response.get('region'))

    @classmethod
    def public_country(cls):
        response = cls.fetch_ip_info()
        return str(response.get('country'))

    @classmethod
    def public_loc(cls):
        response = cls.fetch_ip_info()
        return str(response.get('loc'))

    @classmethod
    def public_org(cls):
        response = cls.fetch_ip_info()
        return str(response.get('org'))

    @classmethod
    def public_postal(cls):
        response = cls.fetch_ip_info()
        return str(response.get('postal'))
    
    @classmethod
    def public_fulladdress(cls):
        response = cls.fetch_ip_info()
        return f"{response.get('city', 'N/A')}, {response.get('region', 'N/A')}, {response.get('country', 'N/A')}, {response.get('postal', 'N/A')}"

    @classmethod
    def public_timezone(cls):
        response = cls.fetch_ip_info()
        return str(response.get('timezone'))

    @classmethod
    def public_all_stats(cls, indent=False):
        response = cls.fetch_ip_info()
        if indent:
            return json.dumps(response, indent=2)
        else:
            return json.dumps(response, indent=None)


    ### -- PRIVATE INFORMATION -- ###
        
    @classmethod
    def private_ip(cls):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            private_ip = s.getsockname()[0]
        return str(private_ip)


    ### -- OTHER INFORMATION -- ###

    @classmethod
    def open_ports(cls):
        open_ports_list = []
        ip = socket.gethostbyname (socket.gethostname())
        for port in range(65535):
            try:
                serv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                serv.bind((ip,port))
            except:
                open_ports_list.append(int(port))
            serv.close()
        return open_ports_list

    @classmethod
    def ip_probe(cls, ip_address, indent=False):
        response = requests.get(f"https://ipinfo.io/{ip_address}/json").json()
        if indent:
            return json.dumps(response, indent=2)
        else:
            return json.dumps(response, indent=None)
