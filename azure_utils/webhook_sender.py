
import requests

def send_to_webhook(url, payload):
    response = requests.post(url, json=payload)
    return response.status_code
