'''Tests for the http server
'''

from subprocess import Popen, PIPE
from time import sleep
#import json
#import urllib
import re
import signal
import requests
#import logging
import pytest
import data



# Use this fixture to get the URL of the server.
@pytest.fixture
def url_start_server():
    '''this starts the server & generates and url'''
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
    '''Check server set up properly'''
    assert url.startswith("http")

def test_system(url):
    '''This is a test where two users access all the functions in flocker
    '''

    #### ----- REGISTER USER1 ----- ####
    input_value = {
        'email': 'captainunderpants@gmail.com',
        'password': 'valid12345',
        'name_first': 'Captain',
        'name_last': 'Underpants'
    }
    data = requests.post(f"{url}/auth/register", json = input_value)

    # Checking good connection
    assert data.status_code == 200

    # Check return values
    payload = data.json()
    assert payload['u_id'] == 1

    token_1 = payload['token']

    #### ----- LOGIN USER1 ----- ####
    input_value = {
        'email': 'captainunderpants@gmail.com',
        'password': 'valid12345'
    }

    data = requests.post(f"{url}/auth/login", json = input_value)

    # Checking good connection
    assert data.status_code == 200

    payload = data.json()
    assert payload['u_id'] == 1
    assert payload['token'] == token_1

    #### ----- LOGOUT USER1 ----- ####
    input_value = {
        'token': registering_token
    }

    data = requests.post(f"{url}/auth/logout", json = input_value)

    payload = data.json()
    assert payload['is_success'] is True

    #### ----- LOGIN USER1 ----- ####
    input_value = {
        'email': 'captainunderpants@gmail.com',
        'password': 'valid12345'
    }

    requests.post(f"{url}/auth/login", json = input_value)

    #### ----- REGISTER & LOGIN USER2 ----- ####
    input_value = {
        'email': 'darthvader@gmail.com',
        'password': 'cool12345',
        'name_first': 'Darth',
        'name_last': 'Vader',
    }

    data = requests.post(f"{url}/auth/register", json = input_value)

    # Check return values
    payload = data.json()
    assert payload['u_id'] == 2

    token_2 = payload['token']

    input_value = {
        'email': 'darthvader@gmail.com',
        'password': 'cool12345'
    }

    requests.post(f"{url}/auth/login", json = input_value)

    #### ----- USER3 ATTEMPTS TO HACK THE LOGIN (INPUT ERROR) ----- ####

    # They remember the email, but not the password of the user.
    input_value = {
        'email': 'darthvader@gmail.com',
        'password': 'camera1234'
    }

    data = requests.post(f"{url}/auth/login", json = input_value)
    assert data.status_code == 400

#------------------------------------------------------------------------------#

    #### ----- USER1 CREATES A CHANNEL ----- ####
    # create public server
    input_value = {
        'token': token_1,
        'name': 'Adventure',
        'is_public': True,
    }

    data = requests.post(f"{url}/channels/create", json = input_value)
    # Checking good connection
    assert data.status_code == 200

    payload = data.json
    assert payload['id'] == 1
    assert payload['name'] == 'Adventure'
    assert payload['is_public'] == True

    #### ----- USER1 INVITES USER2 TO CHANNEL ----- ####
    input_value = {
        'token': token_1,
        'channel_id': 1,
        'u_id': 2,
    }

    data = requests.post(f"{url}/channel/invite", json = input_value)
    # Checking good connection
    assert data.status_code == 200

    payload = data.json()
    assert payload = {}

    #### ----- USER1 CHECKS CHANNEL DETAILS ----- ####
    input_value = {
        'token': token_1,
        'channel_id': 1,
    }

    data = requests.get(f"{url}/channel/details", json = input_value)
    # Checking good connection
    assert data.status_code == 200

    payload = data.json()
    assert payload['name'] == 'Adventure'
    assert payload['owner_members'] == [1]
    assert payload['all_members'] == [1, 2]

    #### ----- USER2 LEAVES THE CHANNEL ----- ####
    input_value = {
        'token': token_2,
        'channel_id': 1
    }

    data = requests.post(f"{url}/channel/leave", json = input_value)
    # Checking good connection
    assert data.status_code == 200

    payload = data.json()
    assert payload = {}

    #### ----- USER1 CHECKS CHANNEL DETAILS ----- ####
    input_value = {
        'token': token_1,
        'channel_id': 1
    }

    data = requests.get(f"{url}/channel/details", json = input_value)
    payload = data.json()

    assert payload['name'] == 'Adventure'
    assert payload['owner_members'] == [1]
    assert payload['all_members'] == [1]

    #### ----- USER2 CHECKS CHANNEL DETAILS (ACCESS ERROR) ----- ####
    input_value = {
        'token': token_2,
        'channel_id': 1
    }

    data = requests.get(f"{url}/channel/details", json = input_value)

    assert data.status_code == 403

    #### ----- USER2 JOINS THE CHANNEL ----- ####
    input_value = {
        'token': token_2,
        'channel_id': 1
    }

    data = requests.post(f"{url}/channel/join", json = input_value)
    # Checking good connection
    assert data.status_code == 200

    payload = data.getjson()
    assert payload = {}

    ### --- USER3 ATTEMPTS TO HACK IN AND JOIN A CHANNEL (ACCESS ERROR) --- ###
    input_value = {
        'token': 'hacker_token_will_not_work',
        'channel_id': 1
    }

    data = requests.post(f"{url}/channel/join", json = input_value)
    assert data.status_code == 401

    #### ----- USER2 CHECKS CHANNEL DETAILS ----- ####
    input_value = {
        'token': token_2,
        'channel_id': 1
    }

    data = requests.get(f"{url}/channel/details", json = input_value)
    payload = data.json()

    assert payload['name'] == 'Adventure'
    assert payload['owner_members'] == [1]
    assert payload['all_members'] == [1, 2]

    #### ----- USER1 ADDS USER2 AS OWNER ----- ####
    input_value = {
        'token': token_1,
        'channel_id': 1,
        'u_id': 2
    }

    data = requests.post(f"{url}/channel/addowner", json = input_value)
    # Checking good connection
    assert data.status_code == 200

    payload = data.getjson()
    assert payload == {}

    #### ----- USER1 CHECKS CHANNEL DETAILS ----- ####
    input_value = {
        'token': token_1,
        'channel_id': 1,
    }

    data = requests.get(f"{url}/channel/details", json = input_value)
    payload = data.json()

    assert payload['name'] == 'Adventure'
    assert payload['owner_members'] == [1, 2]
    assert payload['all_members'] == [1, 2]

    #### ----- USER1 REMOVES USER2 AS OWNER ----- ####
    input_value = {
        'token': token_1,
        'channel_id': 1,
        'u_id': 2,
    }

    data = requests.post(f"{url}/channel/removeowner", json = input_value)
    # Checking good connection
    assert data.status_code == 200

    payload = data.getjson()
    assert payload == {}

    #### ----- USER1 CHECKS CHANNEL DETAILS ----- ####
    input_value = {
        'token': token_1,
        'channel_id': 1,
    }

    data = requests.get(f"{url}/channel/details", json = input_value)
    payload = data.json()

    assert payload['name'] == 'Adventure'
    assert payload['owner_members'] == [1]
    assert payload['all_members'] == [1, 2]

#------------------------------------------------------------------------------#

    # message/send test
    #### ---- USER1 SENDS MESSAGE ----- ####
    input_value = {
        'token': token_1,
        'channel_id': 1,
        'message': 'Never underestimate the power of Captain Underpants!'
    }

    data = requests.post(f"{url}/message/send", json = input_value)
    payload = data.getjson()
    assert payload['message_id'] == 1

    #### ---- USER2 SENDS MESSAGE ----- ####
    input_value = {
        'token': token_2,
        'channel_id': 1,
        'message': 'I will show you the power of the Dark Side of the Force'
    }

    data = requests.post(f"{url}/message/send", json = input_value)
    payload = data.getjson()
    assert payload['message_id'] == 2

    # message/edit test
    #### ---- USER1 EDITS MESSAGE ----- ####
    input_value = {
        'token': token_1,
        'message_id': 1,
        'message': 'Hello black tin can'
    }

    data = requests.put(f"{url}/message/edit", json = input_value)
    payload = data.getjson()
    assert payload == {}

    # message/remove test
    #### ---- USER1 DELETES MESSAGE ----- ####
    input_value = {
        'token': token_1,
        'message_id': 2
    }

    data = requests.delete(f"{url}/message/remove", json = input_value)
    payload = data.getjson()
    assert payload == {}

    #channel/messages
    #### ---- USER1 RETRIEVES MESSAGES ----- ####
    input_value = {
        'token': 'captainunderpants@gmail.com',
        'channel_id': 1,
        'start': 1,
    }
    data = requests.get(f"{url}/channel/details", json = input_value)
    payload = data.getjson()

    assert payload['messages'] == ['Hello black tin can']
    assert payload['start'] == 1
    assert payload['end'] == 51


    #channels/list
    input_value = {
        'token': token_1
    }

    data = requests.get(f"{url}/channels/list", json = input_value)
    payload = data.json()

    assert payload['channels'] == [ {'channel_id': 1, 'name': 'Adventure' } ]

    #channels/listall
    #### ---- USER1 RETRIEVES ALL CHANNELS DETAILS ----- ####
    input_value = {
        'token': token_1
    }

    data = requests.get(f"{url}/channels/listall", json = input_value)
    payload = data.json()

    assert payload['channels'] == [{'channel_id': 1, 'name': 'Adventure' }]

    #user/profile/setname
    #### ---- USER2 CHANGES NAME ----- ####
    input_value = {
        'token': token_2,
        'name_first': 'Anakin',
        'name_last': 'Skywalker',
    }

    data = requests.put(f"{url}/user/profile/setname",json = input_value)
    payload = data.getjson()

    assert payload == {}

    # user/profile/setemail
    #### ---- USER2 CHANGES EMAIL ----- ####
    input_value = {

        'token': 'darthvader@gmail.com',
        'email': 'anakinskywalker@gmail.com',
    }

    data = requests.put(f"{url}/user/profile/setemail",json = input_value)
    payload = data.getjson()

    assert payload = {}


    #user/profile/sethandle
    #### ---- USER2 CHANGES HANDLE ----- ####
    input_value = {

        'token': 'darthvader@gmail.com',
        'handlestr': 'askywalker',
    }

    data = requests.put(f"{url}/user/profile/sethandle",json = input_value)
    payload = data.getjson()

    #user/profile
    #### ---- USER2 RETRIEVES USER PROFILE DETAILS ----- ####
    input_value = {
        'token': token_2,
        'u_id': 2,
    }

    data = requests.get(f"{url}/user/profile", json = input_value)
    payload = data.json()

    assert payload['user'] == {
            'u_id': 2,
            'email': 'anakinskywalker@gmail.com',
            'name_first': 'Anakin',
            'name_last': 'Skywalker',
            'handle_str': 'askywalker',
    }

#users/all
    #### ---- USER1 RETRIEVES ALL USER DETAILS ----- ####
    input_value = {
        'token': token_1,
    }

    data = requests.get(f"{url}/users/all", json = input_value)
    payload = data.json()

    assert payload['users'] == [ {
            'u_id': 1,
            'email': 'captainunderpants@gmail.com',
            'name_first': 'Captain',
            'name_last': 'Underpants',
            'handle_str': 'cunderpants',
    },
    {
            'u_id': 2,
            'email': 'anakinskywalker@gmail.com',
            'name_first': 'Anakin',
            'name_last': 'Skywalker',
            'handle_str': 'cskywalker',
    } ]

#admin/userpermission/change
    #### ---- USER1 SETS USER2 PERMISSIONS TO ADMIN ----- ####
    input_value = {

        'token' : token_1,
        'u_id' : 2,
        'permission_id' : 1,
    }

    data = requests.post(f"{url}/admin/userpermission/change", json = input_value)
    payload = data.getjson()

    assert payload == {}

#Search
    #### ---- USER1 RETRIEVES MESSAGES MATCHING QUERY ----- ####
    input_value = {
        'token': token_1,
        'query_str': "black tin can"
    }

    data = requests.get(f"{url}/search", json = input_value)
    payload = data.json()

    assert payload['messages'] == [ {
            'message_id': 1,
            'u_id': 1,
            'message': 'Hello black tin can',

            #Check this before merging it together
            'time_created': 1582426789,

    } ]

#Clear

    data = requests.delete(f"{url}/delete")
    payload = data.getjson()

    assert payload == {}
