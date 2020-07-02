import json
import os
import random
import sys
import time
import uuid

from time import gmtime, strftime

from faker import Faker
from faker.providers import address
from faker.providers import internet

import arrow
import requests

# Python HTTP Client for the Azure Logic App.
# Chris Joakim, Microsoft, 2020/06/29
#
# Usage:
# $ python http_client.py invoke_http_logic_app 

STATES = 'VA,TN,AL,NC,SC'.split(',')

fake = Faker()
fake.add_provider(address)
fake.add_provider(internet)

def invoke_http_logic_app():
    # Generate and HTTP Post a randomized JSON document to the Azure Logic App
    # A generated document looks like this:
    # {'pk': 'E', 'epoch': 1593443622, 'x': 'X-70948', 'y': 'Y-6834'}

    url = os.environ['AZURE_LOGICAPP_URL']
    headers = {'Content-Type': 'application/json'}
    body = {}
    body['id'] = str(uuid.uuid4())
    body['pk'] = random.choice(STATES)
    body['epoch'] = arrow.utcnow().timestamp
    body['doctype'] = 'logic_app_post'

    # https://github.com/joke2k/faker/blob/master/tests/providers/test_address.py
    body['name'] = fake.name()
    body['city'] = fake.city()
    body['address'] = '{} {} {}'.format(
        fake.building_number(), fake.street_name(), fake.street_suffix())
    body['state'] = fake.state()
    body['message'] = fake.text()

    body['x']  = 'X-{}'.format(str(int(random.random() * 100000)))
    body['y']  = 'Y-{}'.format(str(int(random.random() * 100000)))
    execute_post(url, headers, body)

def execute_post(url, headers, body):
    jstr = json.dumps(body)
    print('POST to: {}'.format(url))
    print('headers: {}'.format(headers))
    print('body:    {}'.format(json.dumps(body, indent=2)))
    r = requests.post(url, headers=headers, data=jstr)
    print('respone code:    {}'.format(r.status_code))
    print('respone headers: {}'.format(r.headers))
    print('respone text:    {}'.format(r.text))

def explore_faker():
    states = dict()
    for n in range(100000):
        s = fake.state()
        states[s] = n
    print(json.dumps(states, indent=2, sort_keys=True))

if __name__ == "__main__":

    if len(sys.argv) > 1:
        func  = sys.argv[1].lower()
        if func == 'invoke_http_logic_app':
            invoke_http_logic_app()
        elif func == 'explore_faker':
            explore_faker()
        else:
            print('undefined func: {}'.format(func))
    else:
        print('specify a command line function')

# {
#   "Alabama": 99995,
#   "Alaska": 99972,
#   "Arizona": 99958,
#   "Arkansas": 99980,
#   "California": 99870,
#   "Colorado": 99911,
#   "Connecticut": 99982,
#   "Delaware": 99928,
#   "Florida": 99974,
#   "Georgia": 99992,
#   "Hawaii": 99968,
#   "Idaho": 99985,
#   "Illinois": 99815,
#   "Indiana": 99937,
#   "Iowa": 99903,
#   "Kansas": 99946,
#   "Kentucky": 99977,
#   "Louisiana": 99999,
#   "Maine": 99952,
#   "Maryland": 99808,
#   "Massachusetts": 99971,
#   "Michigan": 99993,
#   "Minnesota": 99997,
#   "Mississippi": 99986,
#   "Missouri": 99930,
#   "Montana": 99936,
#   "Nebraska": 99924,
#   "Nevada": 99991,
#   "New Hampshire": 99940,
#   "New Jersey": 99963,
#   "New Mexico": 99970,
#   "New York": 99758,
#   "North Carolina": 99955,
#   "North Dakota": 99902,
#   "Ohio": 99967,
#   "Oklahoma": 99951,
#   "Oregon": 99900,
#   "Pennsylvania": 99914,
#   "Rhode Island": 99954,
#   "South Carolina": 99907,
#   "South Dakota": 99989,
#   "Tennessee": 99984,
#   "Texas": 99996,
#   "Utah": 99981,
#   "Vermont": 99890,
#   "Virginia": 99998,
#   "Washington": 99880,
#   "West Virginia": 99931,
#   "Wisconsin": 99987,
#   "Wyoming": 99990
# }