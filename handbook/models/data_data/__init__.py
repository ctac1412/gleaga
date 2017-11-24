# -*- coding: utf-8 -*-

import json
import requests



class DaDataClient(object):
    key=''
    secret=''
    def __init__(self, key="",secret=""):
        self.key =key
        self.secret = secret

client = DaDataClient(
    key = 'fbb9c14272bbad42f32f92652fdb8fb661ba9dd3',
    secret = ' 6f7ebcb3726dbfcef16be26ddec9085ef6d15924',
)

def suggest_api(query, resource):
    # resource = party
    try:
        url = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/%s' % resource
        headers = {
            'Authorization': 'Token %s' % client.key,
            'Content-Type': 'application/json',
        }
        data = {
            'query': query
        }
        r = requests.post(url, data=json.dumps(data), headers=headers)
        return r.json()["suggestions"][0]
    except (ValueError, KeyError, TypeError):
        print "-----------------------------------------------" + ValueError

def clean_api(query, resource):
    # resource = {address,
    # phone,
    # passport,
    # name}
    url = 'https://dadata.ru/api/v2/clean/%s' % resource
    headers = {
        'Authorization': 'Token %s' % client.key,
        'X-Secret': client.secret,
        'Content-Type': 'application/json',
    }
    data = [query]
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()[0]
