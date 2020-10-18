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
    assert payload['channel_id'] == 1

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

    assert payload['name'] == 'Adventure'
    assert payload['owner_members'] == [1]
    assert payload['all_members'] == [2]


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

    assert payload['name'] == 'Adventure'
    assert payload['owner_members'] == [1]
    assert payload['all_members'] == []

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

    assert payload['name'] == 'Adventure'
    assert payload['owner_members'] == [1]
    assert payload['all_members'] == [2]

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

    assert payload['name'] == 'Adventure'
    assert payload['owner_members'] == [1,2]
    assert payload['all_members'] == []

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

    assert payload['name'] == 'Adventure'
    assert payload['owner_members'] == [1]
    assert payload['all_members'] == [2]

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
    assert payload == {}

    # message/remove test
    inputValue = {
        'token': 'captainunderpants@gmail.com'
        'message_id': 2
    }

    r = requests.post(f"{url}/message/remove", json = inputValue)
    payload = r.json()
    assert payload == {}


    #channel/messages
    inputValue = {
        'token': 'captainunderpants@gmail.com'
        'channel_id': 1
        'start': 1
    }
    r = requests.get(f"{url}/channel/details", json = inputValue)
    payload = r.json()

    assert payload['messages'] == ['Hello black tin can']
    assert payload['start'] == 1
    assert payload['end'] == 51


    #channels/list
    inputValue = {
        'token': 'captainunderpants@gmail.com'
    }

    r = requests.get(f"{url}/channels/list", json = inputValue)
    payload = r.json()

    assert payload['channels'] == [ {'channel_id': 1, 'name': 'Adventure' } ]

    #channels/listall

    inputValue = {
        'token': 'captainunderpants@gmail.com'
    }

    r = requests.get(f"{url}/channels/listall", json = inputValue)
    payload = r.json()

    assert payload['channels'] == [ {'channel_id': 1, 'name': 'Adventure' } ]

    #user/profile/setname

    inputValue = {

        'token': 'darthvader@gmail.com'
        'name_first': 'Anakin'
        'name_last': 'Skywalker'
    }

    requests.put(f"{url}/user/profile/setname"),json = inputValue)



    # user/profile/setemail

        inputValue = {

            'token': 'darthvader@gmail.com'
            'email': 'anakinskywalker@gmail.com'
        }

        requests.put(f"{url}/user/profile/setemail"),json = inputValue)


    #user/profile/sethandle

        inputValue = {

            'token': 'darthvader@gmail.com'
            'handlestr': 'askywalker'
        }

        requests.put(f"{url}/user/profile/sethandle"),json = inputValue)

    #user/profile

        inputValue = {

            'token': 'darthvader@gmail.com'
            'u_id': 2
        }

        r = requests.get(f"{url}/user/profile", json = inputValue)
        payload = r.json()

        assert payload['user'] == {

                'u_id': 2,
            	'email': 'anakinskywalker@gmail.com',
            	'name_first': 'Anakin',
            	'name_last': 'Skywalker',
            	'handle_str': 'askywalker',
        }

    #users/all

        inputValue = {
            'token': 'captainunderpants@gmail.com'
        }

        r = requests.get(f"{url}/users/all", json = inputValue)
        payload = r.json()

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

        inputValue = {
            'token' = 'captainunderpants@gmail.com'
            'u_id' = 2
            'permission_id' = 1
        }

        r = requests.post(f"{url}/admin/userpermission/change", json = inputValue)
        payload = r.json()

        assert payload == {}

    #Search

        inputValue = {

            'token': 'captainunderpants@gmail.com'
            'query_str': "black tin can"
        }

        r = requests.get(f"{url}/search", json = inputValue)
        payload = r.json()

        assert payload['messages'] == [ {

                'message_id': 1,
                'u_id': 1,
                'message': 'Hello black tin can',

                #Check this before merging it together
                'time_created': 1582426789,

        } ]

    #Clear

        r = requests.delete(f"{url}/delete")
        payload = r.json()

        assert payload == {}
