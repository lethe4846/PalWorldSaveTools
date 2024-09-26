import requests
import base64
import os
from dotenv import load_dotenv
import csv

# Load environment variables from .env file
load_dotenv()

class Palworld:
    def __init__(self):
        ip = os.getenv('REST_HOST')
        port = os.getenv('REST_PORT')
        password = os.getenv('REST_PASS')
        self.base_url = f"http://{ip}:{port}/v1/api"
        auth_str = f'admin:{password}'
        encoded_auth = base64.b64encode(auth_str.encode()).decode('utf-8')
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f"Basic {encoded_auth}"
        }

    def get_info(self):
        return self._request("GET", "/info", {})

    def get_players(self):
        return self._request("GET", "/players", {})

    def get_settings(self):
        return self._request("GET", "/settings", {})

    def get_metrics(self):
        return self._request("GET", "/metrics", {})

    def _request(self, method, path, payload=None):
        url = f"{self.base_url}{path}"
        try:
            response = requests.request(method, url, headers=self.headers, data=payload)
            response.raise_for_status()
            if response.text:
                return response.json()
            return {'message': 'No content returned'}
        except requests.RequestException as e:
            return {'error': str(e)}
        except ValueError as e:
            return {'error': 'Invalid JSON received', 'response': response.text}

def save_info_to_csv(info_data, filename='info.csv'):
    if info_data and isinstance(info_data, dict):
        fieldnames = info_data.keys()
        with open(filename, mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(info_data)
    else:
        print("No valid info data available to write:", info_data)

def save_settings_to_csv(settings_data, filename='settings.csv'):
    if settings_data and isinstance(settings_data, dict):
        fieldnames = settings_data.keys()
        with open(filename, mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(settings_data)
    else:
        print("No valid settings data available to write:", settings_data)

def save_players_to_csv(players_data, filename='players.csv'):
    if 'players' in players_data:
        players = players_data['players']
        fieldnames = ['name', 'accountName', 'playerId', 'userId', 'ip', 'ping', 'location_x', 'location_y', 'level']
        with open(filename, mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(players)
    else:
        print("No 'players' key in data:", players_data)

def save_metrics_to_csv(metrics_data, filename='metrics.csv'):
    if metrics_data and isinstance(metrics_data, dict):
        fieldnames = metrics_data.keys()
        with open(filename, mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(metrics_data)
    else:
        print("No valid metrics data available to write:", metrics_data)
