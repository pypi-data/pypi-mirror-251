import requests

class HttpClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.forefront.ai"

    def post(self, endpoint, data):
        url = self.base_url + endpoint
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.post(url, json=data, headers=headers)
        return response.json()
