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

    states = load_us_states()
    state_abbreviations = sorted(states.keys())

    url = os.environ['AZURE_LOGICAPP_URL']
    headers = {'Content-Type': 'application/json'}
    body = {}
    body['id'] = str(uuid.uuid4())
    body['pk'] = random.choice(state_abbreviations)
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

def load_us_states():
    states = dict()
    with open('data/us_states.csv', 'rt') as f:
        for line in f:
            tokens = line.split(',')
            name, abbrv = tokens[0].strip(), tokens[1].strip()
            states[abbrv] = name
    return states

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
        elif func == 'load_us_states':
            d = load_us_states()
            print(d)
            print(sorted(d.keys()))
        else:
            print('undefined func: {}'.format(func))
    else:
        print('specify a command line function')
