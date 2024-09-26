import mysql.connector

HOST = '135.125.189.240'
PORT = 3306
USER = 'andrei'
PASSWORD = 'bEuz.[3,wU;c`SZ+#7%fp:'

import requests
import base64
import csv

class Palworld:
    def __init__(self, ip, port, password):
        self.base_url = f"http://{ip}:{port}/v1/api"
        auth_str = 'admin:' + password
        encoded_auth = base64.b64encode(auth_str.encode()).decode('utf-8')
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f"Basic {encoded_auth}"
        }

    def get_players(self):
        return self._request("GET", "/players", {})

    def _request(self, method, path, payload=None):
        url = f"{self.base_url}{path}"
        response = requests.request(method, url, headers=self.headers, data=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'Request failed', 'status': response.status_code, 'message': response.text}

def save_players_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['name', 'accountName', 'playerId', 'userId', 'ip', 'ping', 'location_x', 'location_y', 'level']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for server_data in data:
            if 'players' in server_data:
                writer.writerows(server_data['players'])

def fetch_and_save_players_from_all_servers(server_data):
    all_players_data = []
    for launch_id, details in server_data.items():
        pal = Palworld(ip=details['PublicIP'], port=details['RESTAPIPort'], password=details['AdminPassword'])
        players_data = pal.get_players()
        if 'players' in players_data:
            all_players_data.append(players_data)
    save_players_to_csv(all_players_data, 'players.csv')

import mysql.connector

def fetch_data_from_sql(HOST, PORT, USER, PASSWORD):
    conn = mysql.connector.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database="configurations")
    cursor = conn.cursor()
    cursor.execute("SELECT launch_id, PublicIP, AdminPassword, RESTAPIPort FROM configurations")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return {row[0]: {"PublicIP": row[1], "AdminPassword": row[2], "RESTAPIPort": row[3]} for row in result}

server_data = fetch_data_from_sql(HOST, PORT, USER, PASSWORD)
fetch_and_save_players_from_all_servers(server_data)

