import tls_client
import json

# Domyślne nagłówki HTTP używane do zapytań do Instagrama
default_headers = {
    "accept": "*/*",
    "accept-encoding": "deflate",
    "accept-language": "en-US,en;q=0.9",
    "priority": "u=1, i",
    "referer": "https://www.instagram.com/sghwarsaw/",
    "sec-ch-prefers-color-scheme": "dark",
    "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    "sec-ch-ua-full-version-list": '"Chromium";v="136.0.7103.93", "Google Chrome";v="136.0.7103.93", "Not.A/Brand";v="99.0.0.0"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": '""',
    "sec-ch-ua-platform": '"macOS"',
    "sec-ch-ua-platform-version": '"14.5.0"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}

user_id_dict = {}

def get_tls_session():
    # Tworzy nową sesję TLS z losową kolejnością rozszerzeń TLS
    return tls_client.Session(client_identifier="chrome_128", random_tls_extension_order=True)
    

def get_publications(profile_id="", cursor="", number=0, client_sess=None):
    # Pobiera publikacje z profilu Instagrama za pomocą zapytania GraphQL
    url = 'https://www.instagram.com/graphql/query/'
    params = {
        "doc_id": "7950326061742207",  # Identyfikator zapytania GraphQL
        "variables": '{"id":"'+profile_id+'","after":"'+cursor+'","first":'+str(number)+'}'
    }
    response = client_sess.get(url, params=params, headers=default_headers)
    response_data = {}
    print(response.text)
    try:
        # Próba zdekodowania odpowiedzi jako JSON
        response_data = json.loads(response.text)
    except Exception as err:
        print(f'error loading response as response: {err}')
    
    return response_data