'''Tests for the http server'''
from subprocess import Popen, PIPE
from time import sleep
import json
import urllib
import re
import signal
import requests
import logging
import pytest

from data import print_data

# Use this fixture to get the URL of the server.
@pytest.fixture
def url():
    '''this starts the server & generates and url'''
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
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
    '''Check server set up properly'''
    assert url.startswith("http")

def test_system(url):
    '''This is a test where two users access all the functions in flocker
    '''

    ''' ----- REGISTER USER1 ----- '''
    input_value = {
        'email': 'captainunderpants@gmail.com',
        'password': 'valid12345',
        'name_first': 'Captain',
        'name_last': 'Underpants'
    }

    data = requests.post(str(url) + "auth/register", json=input_value)

    ''' Checking good connection '''
    assert data.status_code == 200

    ''' Check return values '''
    payload = data.json()
    assert payload['u_id'] == 1

    token_1 = payload['token']
    user_1 = payload['u_id']

    ''' ----- LOGIN USER1 ----- '''
    input_value = {
        'email': 'captainunderpants@gmail.com',
        'password': 'valid12345'
    }

    data = requests.post(f"{url}/auth/login", json=input_value)

    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload['u_id'] == user_1
    assert payload['token'] == token_1

    ''' ----- LOGOUT USER1 ----- '''
    input_value = {
        'token': token_1
    }

    data = requests.post(f"{url}/auth/logout", json=input_value)
    
    payload = data.json()
    assert payload['is_success'] is True

    ''' ----- LOGIN USER1 ----- '''
    input_value = {
        'email': 'captainunderpants@gmail.com',
        'password': 'valid12345'
    }

    requests.post(f"{url}/auth/login", json=input_value)

    ''' ----- REGISTER & LOGIN USER2 ----- '''
    input_value = {
        'email': 'darthvader@gmail.com',
        'password': 'cool12345',
        'name_first': 'Darth',
        'name_last': 'Vader',
    }

    data = requests.post(f"{url}/auth/register", json=input_value)

    ''' Check return values '''
    payload = data.json()

    user_2 = payload['u_id']
    assert isinstance(user_2, int)
    token_2 = payload['token']

    input_value = {
        'email': 'darthvader@gmail.com',
        'password': 'cool12345'
    }

    data = requests.post(f"{url}/auth/login", json=input_value)
    
    payload = data.json()
    assert payload['u_id'] == user_2
    assert payload['token'] == token_2

    ''' ----- USER3 ATTEMPTS TO HACK THE LOGIN (INPUT ERROR) ----- '''

    ''' They remember the email, but not the password of the user.'''
    input_value = {
        'email': 'darthvader@gmail.com',
        'password': 'camera1234'
    }

    data = requests.post(f"{url}/auth/login", json=input_value)
    assert data.status_code == 401

#------------------------------------------------------------------------------#

    ''' ----- USER1 CREATES A CHANNEL ----- '''
    ''' create public server '''
    input_value = {
        'token': token_1,
        'name': 'Adventure',
        'is_public': True
    }

    data = requests.post(f"{url}/channels/create", json=input_value)
    
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert isinstance(payload['channel_id'], int)
    channel_0 = payload['channel_id']

    ''' ----- USER1 INVITES USER2 TO CHANNEL ----- '''
    input_value = {
        'token': token_1,
        'channel_id': channel_0,
        'u_id': user_2
    }

    data = requests.post(f"{url}/channel/invite", json=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

    ''' ----- USER1 CHECKS CHANNEL DETAILS ----- '''
    input_value = {
        'token': token_1,
        'channel_id': channel_0,
    }

    data = requests.get(f"{url}/channel/details", params=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload['name'] == 'Adventure'
    assert len(payload['owner_members']) == 1
    assert len(payload['all_members']) == 2

    ''' ----- USER2 LEAVES THE CHANNEL ----- '''
    input_value = {
        'token': token_2,
        'channel_id': channel_0
    }

    data = requests.post(f"{url}/channel/leave", json=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

    ''' ----- USER1 CHECKS CHANNEL DETAILS ----- '''
    input_value = {
        'token': token_1,
        'channel_id': channel_0
    }

    data = requests.get(f"{url}/channel/details", params=input_value)
    payload = data.json()

    assert payload['name'] == 'Adventure'
    assert len(payload['owner_members']) == 1
    assert len(payload['all_members']) == 1

    ''' ----- USER2 CHECKS CHANNEL DETAILS (ACCESS ERROR) ----- '''
    input_value = {
        'token': token_2,
        'channel_id': channel_0
    }

    data = requests.get(f"{url}/channel/details", params=input_value)

    assert data.status_code == 403

    ''' ----- USER2 JOINS THE CHANNEL ----- '''
    input_value = {
        'token': token_2,
        'channel_id': channel_0
    }

    data = requests.post(f"{url}/channel/join", json=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

    ''' --- USER3 ATTEMPTS TO HACK IN AND JOIN A CHANNEL (ACCESS ERROR) --- '''
    input_value = {
        'token': 'hacker_token_will_not_work',
        'channel_id': channel_0
    }

    data = requests.post(f"{url}/channel/join", json=input_value)
    assert data.status_code == 401

    ''' ----- USER2 CHECKS CHANNEL DETAILS ----- '''
    input_value = {
        'token': token_2,
        'channel_id': channel_0,
    }

    data = requests.get(f"{url}/channel/details", params=input_value)
    payload = data.json()

    assert payload['name'] == 'Adventure'
    assert len(payload['owner_members']) == 1
    assert len(payload['all_members']) == 2

    ''' ----- USER1 ADDS USER2 AS OWNER ----- '''
    input_value = {
        'token': token_1,
        'channel_id': channel_0,
        'u_id': user_2
    }

    data = requests.post(f"{url}/channel/addowner", json=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

    ''' ----- USER1 CHECKS CHANNEL DETAILS ----- '''
    input_value = {
        'token': token_1,
        'channel_id': channel_0,
    }

    data = requests.get(f"{url}/channel/details", params=input_value)
    payload = data.json()

    assert payload['name'] == 'Adventure'
    assert len(payload['owner_members']) == 2
    assert len(payload['all_members']) == 2

    ''' ----- USER1 REMOVES USER2 AS OWNER ----- '''
    input_value = {
        'token': token_1,
        'channel_id': channel_0,
        'u_id': user_2,
    }

    data = requests.post(f"{url}/channel/removeowner", json=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

    ''' ----- USER1 CHECKS CHANNEL DETAILS ----- '''
    input_value = {
        'token': token_1,
        'channel_id': channel_0,
    }

    data = requests.get(f"{url}/channel/details", params=input_value)
    payload = data.json()

    assert payload['name'] == 'Adventure'
    assert len(payload['owner_members']) == 1
    assert len(payload['all_members']) == 2
    
#------------------------------------------------------------------------------#

    ''' ---- USER1 SENDS MESSAGE ----- '''
    input_value = {
        'token': token_1,
        'channel_id': channel_0,
        'message': 'Never underestimate the power of Captain Underpants!'
    }

    data = requests.post(f"{url}/message/send", json=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200
    
    payload = data.json()
    assert isinstance(payload['message_id'], int)
    message_1 = payload['message_id']

    ''' ---- USER2 SENDS MESSAGE ----- '''
    input_value = {
        'token': token_2,
        'channel_id': channel_0,
        'message': 'I will show you the power of the Dark Side of the Force'
    }

    data = requests.post(f"{url}/message/send", json=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200
    
    payload = data.json()
    assert isinstance(payload['message_id'], int)
    payload['message_id']

    ''' ---- USER2 CHECKS CHANNEL MESSAGES ----- '''
    input_value = {
        'token': token_2,
        'channel_id': channel_0,
        'start': 0
    }
    
    data = requests.get(f"{url}/channel/messages", params=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200
    
    payload = data.json()
    assert len(payload['messages']) == 2
    
    ''' ---- USER1 EDITS MESSAGE ----- '''
    input_value = {
        'token': token_1,
        'message_id': message_1,
        'message': 'Hello black tin can'
    }

    data = requests.put(f"{url}/message/edit", json=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}
    
    ''' ---- USER1 RETRIEVES CHANNEL MESSAGES ----- '''
    input_value = {
        'token': token_1,
        'channel_id': channel_0,
        'start': 0,
    }
    
    data = requests.get(f"{url}/channel/messages", params=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    
    assert len(payload['messages']) == 2

    ''' ---- USER1 DELETES MESSAGE ----- '''
    input_value = {
        'token': token_1,
        'message_id': message_1
    }

    data = requests.delete(f"{url}/message/remove", json=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

    ''' ---- USER1 RETRIEVES CHANNEL MESSAGES ----- '''
    input_value = {
        'token': token_1,
        'channel_id': channel_0,
        'start': 0,
    }
    
    data = requests.get(f"{url}/channel/messages", params=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert len(payload['messages']) == 1
    assert payload['messages'][0]['message'] == 'I will show you the power of the Dark Side of the Force'

    ''' ---- USER1 RETRIEVES CHANNEL LIST ----- '''
    input_value = {
        'token': token_1
    }

    data = requests.get(f"{url}/channels/list", params=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert len(payload['channels']) == 1
    assert payload['channels'] == [{'channel_id': 0, 'name': 'Adventure' }]
    
    ''' ---- USER2 CREATES A CHANNEL ----- '''
    input_value = {
        'token': token_2,
        'name': 'Advent',
        'is_public': False
    }

    data = requests.post(f"{url}/channels/create", json=input_value)
    
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert isinstance(payload['channel_id'], int)
    payload['channel_id']

    ''' ---- USER1 RETRIEVES ALL CHANNELS DETAILS ----- '''
    input_value = {
        'token': token_1
    }

    data = requests.get(f"{url}/channels/listall", params=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert len(payload['channels']) == 2

    ''' ---- USER2 CHANGES NAME ----- '''
    input_value = {
        'token': token_2,
        'name_first': 'Anakin',
        'name_last': 'Skywalker',
    }

    data = requests.put(f"{url}/user/profile/setname",json=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

    ''' ---- USER2 CHANGES EMAIL ----- '''
    input_value = {

        'token': token_2,
        'email': 'anakinskywalker@gmail.com',
    }

    data = requests.put(f"{url}/user/profile/setemail",json=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

    ''' ---- USER2 CHANGES HANDLE ----- '''
    input_value = {
        'token': token_2,
        'handle_str': 'askywalker',
    }

    data = requests.put(f"{url}/user/profile/sethandle", json=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

    ''' ---- USER2 RETRIEVES USER PROFILE DETAILS ----- '''
    input_value = {
        'token': token_2,
        'u_id': user_2,
    }

    data = requests.get(f"{url}/user/profile", params=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload['user']['email'] == 'anakinskywalker@gmail.com'
    assert payload['user']['name_first'] == 'Anakin'
    assert payload['user']['name_last'] == 'Skywalker'
    assert payload['user']['handle_str'] == 'askywalker'

    ''' ---- USER1 RETRIEVES ALL USER DETAILS ----- '''
    input_value = {
        'token': token_1,
    }

    data = requests.get(f"{url}/users/all", params=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert len(payload['users']) == 2

    ''' ---- USER1 SETS USER2 PERMISSIONS TO ADMIN ----- '''
    input_value = {

        'token' : token_1,
        'u_id' : user_2,
        'permission_id' : 1,
    }

    data = requests.post(f"{url}/admin/userpermission/change", json=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

    ''' ---- USER1 RETRIEVES CHANNEL MESSAGES ----- '''
    input_value = {
        'token': token_1,
        'channel_id': channel_0,
        'start': 0,
    }
    
    data = requests.get(f"{url}/channel/messages", params=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert len(payload['messages']) == 1
    assert payload['messages'][0]['message'] == 'I will show you the power of the Dark Side of the Force'
    
    ''' ---- USER1 RETRIEVES MESSAGES MATCHING QUERY ----- '''
    input_value = {
        'token': token_1,
        'query_str': 'show'
    }

    data = requests.get(f"{url}/search", params=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert len(payload['messages']) == 1

    ''' Clear '''

    data = requests.delete(f"{url}/clear")
    payload = data.json()

    ''' Checking good connection '''
    assert data.status_code == 200
    assert payload == {}
