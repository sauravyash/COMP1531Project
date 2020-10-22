'''
import pytest
import re
import signal
import requests
import logging
import urllib
import json
#import data
from time import sleep
from flask import request
from subprocess import Popen, PIPE
# Use this fixture to get the URL of the server.
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "simple.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")


def test_url(url):
    # Check server set up properly
    assert url.startswith("http")

def test_system(url):

    # register test
    inputValue = {
        'email': 'captainunderpants@gmail.com'
        'password': 'valid12345'
        'name_first': 'Captain'
        'name_last': 'Underpants'
    }
    r = requests.post(f"{url}/auth/register", json = inputValue)

    # Checking good connection
    assert r.status_code == 200

    payload = r.json()
    assert payload['u_id'] == 1
    assert payload['token'] == 'captainunderpants@gmail.com'

    # login test
    inputValue = {
        'email': 'captainunderpants@gmail.com'
        'password': 'valid12345'
    }

    r = requests.post(f"{url}/auth/login", json = inputValue)

    # Checking good connection
    assert r.status_code == 200

    payload = r.json()
    assert payload['u_id'] == 1
    assert payload['token'] == 'captainunderpants@gmail.com'

    # logout test
    inputValue = {
        'token': 'captainunderpants@gmail.com'
    }
    r = requests.post(f"{url}/auth/logout", json = inputValue)
    payload = r.json()
    assert payload['is_success'] == True

    # log back in
    inputValue = {
        'email': 'captainunderpants@gmail.com'
        'password': 'valid12345'
    }
    requests.post(f"{url}/auth/login", json = inputValue)

    # register and login 2nd user
    inputValue = {
        'email': 'darthvader@gmail.com'
        'password': 'cool12345'
        'name_first': 'Darth'
        'name_last': 'Vader'
    }
    requests.post(f"{url}/auth/register", json = inputValue)

    inputValue = {
        'email': 'darthvader@gmail.com'
        'password': 'cool12345'
    }   
    requests.post(f"{url}/auth/login", json = inputValue)

    # channel create test
    # create public server
    inputValue = {
        'token': 'captainunderpants@gmail.com'
        'name': 'Adventure'
        'is_public': True
    }

    r = requests.post(f"{url}/channels/create", json = inputValue)
    payload = r.json
    assert payload['channel_id'] = 1

    # channel invite + channel_detail test
    inputValue = {
        'token': 'captainunderpants@gmail.com'
        'channel_id': 1
        'u_id': 2
    }

    r = requests.post(f"{url}/channel/invite", json = inputValue)
    #payload = r.json()
    #assert payload = {}

    inputValue = {
        'token': 'captainunderpants@gmail.com'
        'channel_id': 1
    }
    
    r = requests.get(f"{url}/channel/details", json = inputValue)
    payload = r.json()

    assert payload['name'] = 'Adventure'
    assert payload['owner_members'] = [1]
    assert payload['all_members'] = [2]


    # channel leave
    inputValue = {
        'token': 'darthvader@gmail.com'
        'channel_id': 1
    }

    r = requests.post(f"{url}/channel/leave", json = inputValue)
    #payload = r.json()
    #assert payload = {}

    inputValue = {
        'token': 'captainunderpants@gmail.com'
        'channel_id': 1
    }
    
    r = requests.get(f"{url}/channel/details", json = inputValue)
    payload = r.json()

    assert payload['name'] = 'Adventure'
    assert payload['owner_members'] = [1]
    assert payload['all_members'] = []

    # channel join
    inputValue = {
        'token': 'darthvader@gmail.com'
        'channel_id': 1
    }
    r = requests.post(f"{url}/channel/join", json = inputValue)

    inputValue = {
        'token': 'captainunderpants@gmail.com'
        'channel_id': 1
    }
    
    r = requests.get(f"{url}/channel/details", json = inputValue)
    payload = r.json()

    assert payload['name'] = 'Adventure'
    assert payload['owner_members'] = [1]
    assert payload['all_members'] = [2]

    # channel addowner
    inputValue = {
        'token': 'captainunderpants@gmail.com'
        'channel_id': 1
        'u_id': 2
    }
    r = requests.post(f"{url}/channel/addowner", json = inputValue)

    inputValue = {
        'token': 'captainunderpants@gmail.com'
        'channel_id': 1
    }
    
    r = requests.get(f"{url}/channel/details", json = inputValue)
    payload = r.json()

    assert payload['name'] = 'Adventure'
    assert payload['owner_members'] = [1,2]
    assert payload['all_members'] = []

    # channel removeowner
    inputValue = {
        'token': 'captainunderpants@gmail.com'
        'channel_id': 1
        'u_id': 2
    }
    r = requests.post(f"{url}/channel/removeowner", json = inputValue)

    inputValue = {
        'token': 'captainunderpants@gmail.com'
        'channel_id': 1
    }
    
    r = requests.get(f"{url}/channel/details", json = inputValue)
    payload = r.json()

    assert payload['name'] = 'Adventure'
    assert payload['owner_members'] = [1]
    assert payload['all_members'] = [2]

    # message/send test
    inputValue = {
        'token': 'captainunderpants@gmail.com'
        'channel_id': 1
        'message': 'Never underestimate the power of Captain Underpants!'
    }

    r = requests.post(f"{url}/message/send", json = inputValue)
    payload = r.json()
    assert payload['message_id'] == 1

    inputValue = {
        'token': 'darthvader@gmail.com'
        'channel_id': 1
        'message': 'I will show you the power of the Dark Side of the Force'
    }

    r = requests.post(f"{url}/message/send", json = inputValue)
    payload = r.json()
    assert payload['message_id'] == 2

    # message/edit test
    inputValue = {
        'token': 'captainunderpants@gmail.com'
        'message_id': 1
        'message': 'Hello black tin can'
    }

    r = requests.post(f"{url}/message/edit", json = inputValue)
    payload = r.json()
    assert payload = {}

    # message/remove test
    inputValue = {
        'token': 'captainunderpants@gmail.com'
        'message_id': 2
    }

    r = requests.post(f"{url}/message/remove", json = inputValue)
    payload = r.json()
    assert payload = {}


    #channel/messages
    inputValue = {
        'token': 'captainunderpants@gmail.com'
        'channel_id': 1
        'start': 1
    }
    r = requests.get(f"{url}/channel/details", json = inputValue)
    payload = r.json()

    assert payload['messages'] =
    assert payload['start'] =
    assert payload['end'] = 
'''