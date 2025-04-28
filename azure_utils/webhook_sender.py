
import requests

def send_to_webhook(url, payload):
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Webhook call failed with status code {response.status_code}: {response.text}")
    return response.status_code
