import requests
import os
from urllib.parse import urlencode
import json


class Nux:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.nux.ai/v1"

    def run(self, workbook_id, parameters):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        url = f"{self.base_url}/run/workbook/{workbook_id}"
        response = requests.post(url, headers=headers, json=parameters)

        # Handle the response
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
