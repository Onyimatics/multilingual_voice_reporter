
import requests

def translate_text(text, key, region, to_lang='en'):
    endpoint = "https://api.cognitive.microsofttranslator.com"
    path = '/translate?api-version=3.0'
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json'
    }
    body = [{'text': text}]
    params = {'to': to_lang}
    response = requests.post(endpoint + path, params=params, headers=headers, json=body)
    return response.json()[0]['translations'][0]['text']
