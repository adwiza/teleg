import requests

from settings import TOKEN, CHAT_ID


server = 'https://api.telegram.org'
endpoint = 'sendMessage'

url = server + '/' + TOKEN + '/' + endpoint

response = requests.post(url, json={'text': 'Привет из питона в группу мои боты', 'chat_id': CHAT_ID})

if response.status_code == 200:
    print(response.json())
