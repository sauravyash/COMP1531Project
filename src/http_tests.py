'''these are the tests for the http server'''
from subprocess import Popen, PIPE
from time import sleep
#import json
#import urllib
import re
import signal
import requests
#import logging
import pytest
#import data



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
    '''This is a test about two users accessing all the functions in flocker'''
    # register test
    input_value = {
        'email': 'captainunderpants@gmail.com',
        'password': 'valid12345',
        'name_first': 'Captain',
        'name_last': 'Underpants'
    }
    data = requests.post(f"{url}/auth/register", json = input_value)

    # Checking good connection
    assert data.status_code == 200

    payload = data.json()
    assert payload['u_id'] == 1
    assert payload['token'] == 'captainunderpants@gmail.com'

    # login test
    input_value = {
        'email': 'captainunderpants@gmail.com',
        'password': 'valid12345'
    }

    data = requests.post(f"{url}/auth/login", json = input_value)

    # Checking good connection
    assert data.status_code == 200

    payload = data.json()
    assert payload['u_id'] == 1
    assert payload['token'] == 'captainunderpants@gmail.com'

    # logout test
    input_value = {
        'token': 'captainunderpants@gmail.com'
    }
    data = requests.post(f"{url}/auth/logout", json = input_value)
    payload = data.json()
    assert payload['is_success'] is True

    # log back in
    input_value = {
        'email': 'captainunderpants@gmail.com',
        'password': 'valid12345'
    }
    requests.post(f"{url}/auth/login", json = input_value)

    # register and login 2nd user
    input_value = {
        'email': 'darthvader@gmail.com',
        'password': 'cool12345',
        'name_first': 'Darth',
        'name_last': 'Vader',
    }
    requests.post(f"{url}/auth/register", json = input_value)

    input_value = {
        'email': 'darthvader@gmail.com',
        'password': 'cool12345'
    }
    requests.post(f"{url}/auth/login", json = input_value)

    # channel create test
    # create public server
    input_value = {
        'token': 'captainunderpants@gmail.com',
        'name': 'Adventure',
        'is_public': True,
    }

    data = requests.post(f"{url}/channels/create", json = input_value)
    payload = data.json
    assert payload['channel_id'] == 1

    # channel invite + channel_detail test
    input_value = {
        'token': 'captainunderpants@gmail.com',
        'channel_id': 1,
        'u_id': 2,
    }

    data = requests.post(f"{url}/channel/invite", json = input_value)
    #payload = data.json()
    #assert payload = {}

    input_value = {
        'token': 'captainunderpants@gmail.com',
        'channel_id': 1,
    }

    data = requests.get(f"{url}/channel/details", json = input_value)
    payload = data.json()

    assert payload['name'] == 'Adventure'
    assert payload['owner_members'] == [1]
    assert payload['all_members'] == [2]


    # channel leave
    input_value = {
        'token': 'darthvader@gmail.com',
        'channel_id': 1
    }

    data = requests.post(f"{url}/channel/leave", json = input_value)
    #payload = data.json()
    #assert payload = {}

    input_value = {
        'token': 'captainunderpants@gmail.com',
        'channel_id': 1
    }

    data = requests.get(f"{url}/channel/details", json = input_value)
    payload = data.json()

    assert payload['name'] == 'Adventure'
    assert payload['owner_members'] == [1]
    assert payload['all_members'] == []

    # channel join
    input_value = {
        'token': 'darthvader@gmail.com',
        'channel_id': 1
    }
    data = requests.post(f"{url}/channel/join", json = input_value)

    input_value = {
        'token': 'captainunderpants@gmail.com',
        'channel_id': 1
    }

    data = requests.get(f"{url}/channel/details", json = input_value)
    payload = data.json()

    assert payload['name'] == 'Adventure'
    assert payload['owner_members'] == [1]
    assert payload['all_members'] == [2]

    # channel addowner
    input_value = {
        'token': 'captainunderpants@gmail.com',
        'channel_id': 1,
        'u_id': 2
    }
    data = requests.post(f"{url}/channel/addowner", json = input_value)

    input_value = {
        'token': 'captainunderpants@gmail.com',
        'channel_id': 1
    }

    data = requests.get(f"{url}/channel/details", json = input_value)
    payload = data.json()

    assert payload['name'] == 'Adventure'
    assert payload['owner_members'] == [1,2]
    assert payload['all_members'] == []

    # channel removeowner
    input_value = {
        'token': 'captainunderpants@gmail.com',
        'channel_id': 1,
        'u_id': 2
    }
    data = requests.post(f"{url}/channel/removeowner", json = input_value)

    input_value = {
        'token': 'captainunderpants@gmail.com',
        'channel_id': 1
    }

    data = requests.get(f"{url}/channel/details", json = input_value)
    payload = data.json()

    assert payload['name'] == 'Adventure'
    assert payload['owner_members'] == [1]
    assert payload['all_members'] == [2]

    # message/send test
    input_value = {
        'token': 'captainunderpants@gmail.com',
        'channel_id': 1,
        'message': 'Never underestimate the power of Captain Underpants!'
    }

    data = requests.post(f"{url}/message/send", json = input_value)
    payload = data.json()
    assert payload['message_id'] == 1

    input_value = {
        'token': 'darthvader@gmail.com',
        'channel_id': 1,
        'message': 'I will show you the power of the Dark Side of the Force'
    }

    data = requests.post(f"{url}/message/send", json = input_value)
    payload = data.json()
    assert payload['message_id'] == 2

    # message/edit test
    input_value = {
        'token': 'captainunderpants@gmail.com',
        'message_id': 1,
        'message': 'Hello black tin can'
    }

    data = requests.post(f"{url}/message/edit", json = input_value)
    payload = data.json()
    assert payload == {}

    # message/remove test
    input_value = {
        'token': 'captainunderpants@gmail.com',
        'message_id': 2
    }

    data = requests.post(f"{url}/message/remove", json = input_value)
    payload = data.json()
    assert payload == {}


    #channel/messages
    input_value = {
        'token': 'captainunderpants@gmail.com',
        'channel_id': 1,
        'start': 1,
    }
    data = requests.get(f"{url}/channel/details", json = input_value)
    payload = data.json()

    assert payload['messages'] == ['Hello black tin can']
    assert payload['start'] == 1
    assert payload['end'] == 51


    #channels/list
    input_value = {
        'token': 'captainunderpants@gmail.com'
    }

    data = requests.get(f"{url}/channels/list", json = input_value)
    payload = data.json()

    assert payload['channels'] == [ {'channel_id': 1, 'name': 'Adventure' } ]

    #channels/listall

    input_value = {
        'token': 'captainunderpants@gmail.com'
    }

    data = requests.get(f"{url}/channels/listall", json = input_value)
    payload = data.json()

    assert payload['channels'] == [ {'channel_id': 1, 'name': 'Adventure' } ]

    #user/profile/setname

    input_value = {

        'token': 'darthvader@gmail.com',
        'name_first': 'Anakin',
        'name_last': 'Skywalker',
    }

    requests.put(f"{url}/user/profile/setname",json = input_value)



    # user/profile/setemail

    input_value = {

        'token': 'darthvader@gmail.com',
        'email': 'anakinskywalker@gmail.com',
    }

    requests.put(f"{url}/user/profile/setemail",json = input_value)


    #user/profile/sethandle

    input_value = {

        'token': 'darthvader@gmail.com',
        'handlestr': 'askywalker',
    }

    requests.put(f"{url}/user/profile/sethandle",json = input_value)

    #user/profile

    input_value = {

        'token': 'darthvader@gmail.com',
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

    input_value = {
        'token': 'captainunderpants@gmail.com',
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

    input_value = {

        'token' : 'captainunderpants@gmail.com',
        'u_id' : 2,
        'permission_id' : 1,
    }

    data = requests.post(f"{url}/admin/userpermission/change", json = input_value)
    payload = data.json()

    assert payload == {}

#Search

    input_value = {

        'token': 'captainunderpants@gmail.com',
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
    payload = data.json()

    assert payload == {}
