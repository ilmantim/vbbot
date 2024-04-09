import requests
import json
from environs import Env

env = Env()
env.read_env()
vb_token = env.str('VB_TOKEN')
url = env.str('HOOK')

hook = 'https://chatapi.viber.com/pa/set_webhook'
headers = {'X-Viber-Auth-Token': vb_token}
sen = dict(
    url=f'https://{url}/viber/',
    event_types=[
         'unsubscribed', 'conversation_started', 'message',
         'delivered', 'subscribed'
    ]
)
r = requests.post(hook, json.dumps(sen), headers=headers)
