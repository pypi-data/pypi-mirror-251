import requests


def translate(text, source_lang='en', target_lang='fr'):
    api_url = "https://655.mtis.workers.dev/translate"
    params = {
        'text': text,
        'source_lang': source_lang,
        'target_lang': target_lang
    }
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(response.json())
    else:
        return f"Translation error: {response.text}"
    
