import requests

ARBITAL_SUBSPACES = ['ai_alignment', 'math', 'rationality']
headers = {
    'authority': 'arbital.com',
    'accept': 'application/json, text/plain, */*',
    'content-type': 'application/json;charset=UTF-8',
    'sec-ch-ua-mobile': '?0',
    'origin': 'https://arbital.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'accept-language': 'en-US,en;q=0.9',
}

def get_page(alias):
    headers['referer'] = 'https://arbital.com/'
    data = f'{{"pageAlias":"{alias}"}}'
    response = requests.post(
        'https://arbital.com/json/primaryPage/', headers=headers, data=data).json()
    return response['pages'][alias]

aliases = []
for subspace in ARBITAL_SUBSPACES:
    headers['referer'] = f'https://arbital.com/explore/{subspace}/'
    data = f'{{"pageAlias":"{subspace}"}}'
    response = requests.post('https://arbital.com/json/explore/', headers=headers, data=data).json()
    aliases.extend(list(response['pages'].keys()))

for alias in aliases:
    page = get_page(alias)
    url = f'https://arbital.com/p/{page["alias"]}/'
    print(url)