import json
import os
import random
import sys
import time
import uuid

from time import gmtime, strftime

from faker import Faker
from faker.providers import address
from faker.providers import barcode
from faker.providers import internet

import arrow
import requests

# Python HTTP Client for the Azure Logic App.
# Simulates a home security system.
# Chris Joakim, Microsoft, 2020/07/03
#
# Usage:
# $ python security_system.py

US_STATES = 'AK,AL,AR,AZ,CA,CO,CT,DC,DE,FL,GA,HI,IA,ID,IL,IN,KS,KY,LA,MA,MD,ME,MI,MN,MO,MS,MT,NC,ND,NE,NH,NJ,NM,NV,NY,OH,OK,OR,PA,RI,SC,SD,TN,TX,UT,VA,VT,WA,WI,WV,WY'.split(',')

# The Faker library is used to create randomized values
fake = Faker()
fake.add_provider(address)
fake.add_provider(barcode)
fake.add_provider(internet)

def post_security_system_message():
    # Generate and HTTP Post a randomized JSON document to the Azure Logic App
    url = os.environ['AZURE_LOGICAPP_URL']
    headers = {'Content-Type': 'application/json'}
    body = generate_message_body()
    execute_post(url, headers, body)

def generate_message_body():
    device = fake.ean(length=13)
    r1 = int(random.random() * 100)
    r2 = int(random.random() * 100)
    r3 = int(random.random() * 100)
    normal_temp = 60 + int(random.random() * 20)
    normal_cv = int(random.random() * 10)
    body = {}
    body['id'] = str(uuid.uuid4())
    body['pk'] = device
    body['device_id'] = device
    body['epoch'] = arrow.utcnow().timestamp
    body['temperature'] = normal_temp  # temperature sensor
    body['cv_threat'] = normal_cv      # computer-vision sensor
    body['name'] = fake.name()
    body['address'] = '{} {} {}'.format(
        fake.building_number(), fake.street_name(), fake.street_suffix())
    body['city'] = fake.city()
    body['state'] = random.choice(US_STATES)
    body['doctype'] = 'home_security_system_heartbeat'
    body['info'] = '{}.{}.{}'.format(r1, r2, r3)

    # 10% of these generated messages will indicate an anomaly
    if r1 < 10:
        if r2 < 50:
            # temperature anomalies
            if r3 < 50:
                body['temperature'] = 500 + int(random.random() * 100)  # house on fire!
                body['cv_threat'] = normal_cv
            else:
                body['temperature'] = 200 + int(random.random() * 50)  # something is burning
                body['cv_threat'] = normal_cv 
        else:
            # cv anomalies
            if r3 < 50:
                body['temperature'] = normal_temp
                body['cv_threat'] = 90 + int(random.random() * 10)  # intruder is in the house!
            else:   
                body['temperature'] = normal_temp
                body['cv_threat'] = 30 + int(random.random() * 50)  # someone is outside
    return body

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

def debug_messages():
    for n in range(100):
        body = generate_message_body()
        t  = body['temperature']
        cv = body['cv_threat']
        t_msg, cv_msg = '', ''
        if t >= 200:
            t_msg = 'warm'
        if t >= 500:
            t_msg = 'fire'
        if cv >= 30:
            cv_msg = 'outside'
        if cv >= 90:
            cv_msg = 'intruder'
        print('{} {} | {} {} | {}'.format(t, t_msg, cv, cv_msg, body['randoms']))

def ad_hoc():
    states = load_us_states()
    state_abbreviations = sorted(states.keys())
    print(states)
    print(state_abbreviations)
    print(','.join(state_abbreviations))


if __name__ == "__main__":

    if len(sys.argv) > 1:
        func = sys.argv[1].lower()
        if func == 'explore_faker':
            explore_faker()
        elif func == 'debug_messages':
            debug_messages()
        elif func == 'ad_hoc':
            ad_hoc()
        elif func == 'load_us_states':
            d = load_us_states()
            print(d)
            print(sorted(d.keys()))
        else:
            print('specify a function on the command-line')
    else:
        post_security_system_message()
