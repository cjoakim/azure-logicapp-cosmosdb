import json
import os
import random
import sys
import time

from time import gmtime, strftime

import arrow
import requests

# Python HTTP Client for the Azure Logic App.
# Chris Joakim, Microsoft, 2020/06/29
#
# Usage:
# $ python http_client.py invoke_http_logic_app 

LETTERS = 'A,B,C,D,E,F,G,H,I,J'.split(',')

def invoke_http_logic_app():
    # Generate and HTTP Post a randomized JSON document to the Azure Logic App
    # A generated document looks like this:
    # {'pk': 'E', 'epoch': 1593443622, 'x': 'X-70948', 'y': 'Y-6834'}

    url = os.environ['AZURE_LOGICAPP_URL']
    headers = {'Content-Type': 'application/json'}
    body = {}
    body['pk'] = random.choice(LETTERS)
    body['epoch'] = arrow.utcnow().timestamp
    body['x']  = 'X-{}'.format(str(int(random.random() * 100000)))
    body['y']  = 'Y-{}'.format(str(int(random.random() * 100000)))
    execute_post(url, headers, body)

def execute_post(url, headers, body):
    jstr = json.dumps(body)
    print('POST to: {}'.format(url))
    print('headers: {}'.format(headers))
    print('body:    {}'.format(body))
    r = requests.post(url, headers=headers, data=jstr)
    print('respone code:    {}'.format(r.status_code))
    print('respone headers: {}'.format(r.headers))
    print('respone text:    {}'.format(r.text))


if __name__ == "__main__":

    if len(sys.argv) > 1:
        func  = sys.argv[1].lower()
        if func == 'invoke_http_logic_app':
            invoke_http_logic_app()
        else:
            print('undefined func: {}'.format(func))
    else:
        print('specify a command line function')
