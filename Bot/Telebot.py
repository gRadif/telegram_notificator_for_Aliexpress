import re

from config import token
import requests


PARAMS_BOT = {'update_id': 0}
BASE_URL =f'https://api.telegram.org/bot{token}/'

class Bot:

    def listen_chat(self):

        update_id = PARAMS_BOT['update_id']
        url = BASE_URL + 'GetUpdates'
        params = {
            'offset': f'{update_id}'
        }
        response = requests.get(url, params=params)
        response = response.json()


        if len(response['result']) >= 1:
            PARAMS_BOT['update_id'] = response['result'][0]['update_id'] + 1
            return response['result']

        else:
            pass

    def send_message(self, chat_id, text ):

        params = {
            'text': text,
            'chat_id': chat_id,
            'parse_mode':'html'
        }
        url = BASE_URL + 'sendMessage'
        response_2 = requests.post(url, params=params)
        # print(response_2.json())



