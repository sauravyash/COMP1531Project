from subprocess import Popen, PIPE
from time import sleep
import json
import urllib
import re
import signal
import requests
import logging
import pytest

# Helpful Globals
# ----- USER1
EMAIL_1 = 'validemail1@gmail.com'
PASSWORD_1 = 'validpassword1234'
NAME_F_1 = 'Tom'
NAME_L_1 = 'Riddles'
# ----- USER2
EMAIL_2 = 'validemail2@gmail.com'
PASSWORD_2 = 'validpassword2234'
NAME_F_2 = 'Timothy'
NAME_L_2 = 'Banks'
# ----- USER3
EMAIL_3 = 'validemail3@gmail.com'
PASSWORD_3 = 'validpassword3234'
NAME_F_3 = 'Alison'
NAME_L_3 = 'Cardigan'

@pytest.fixture()
def url():
    '''this starts the server & generates and url'''
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url: # pragma: no cover
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None: # pragma: no cover
            server.kill()
    else:
        server.kill() # pragma: no cover
        raise Exception("Couldn't get URL from local server") # pragma: no cover

# ----- Clear the server, and provide details of first user.
@pytest.fixture()
def setup_auth(url):
    data = requests.delete(str(url) + "/clear")
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

    input_reg = [
        {
            'email': EMAIL_1,
            'password': PASSWORD_1,
            'name_first': NAME_F_1,
            'name_last': NAME_L_1
        },
        {
            'email': EMAIL_2,
            'password': PASSWORD_2,
            'name_first': NAME_F_2,
            'name_last': NAME_L_2
        },
        {
            'email': EMAIL_3,
            'password': PASSWORD_3,
            'name_first': NAME_F_3,
            'name_last': NAME_L_3
        }
    ]
    
    input_log = [
        {
            'email': EMAIL_1,
            'password': PASSWORD_1,
        },
        {
            'email': EMAIL_2,
            'password': PASSWORD_2,
        },
        {
            'email': EMAIL_3,
            'password': PASSWORD_3,
        }
    ]

    return input_reg, input_log

# ---------------------------------------------------------------------------- #
''' AUTH FIXTURES '''

@pytest.fixture()
def register_user(url, setup_auth):
    input_value, _ = setup_auth

    data = requests.post(str(url) + "auth/register", json=input_value[0])
    assert data.status_code == 200
    user1 = data.json()
    
    data = requests.post(str(url) + "auth/register", json=input_value[1])
    assert data.status_code == 200
    user2 = data.json()
    
    data = requests.post(str(url) + "auth/register", json=input_value[2])
    assert data.status_code == 200
    user3 = data.json()

    return user1, user2, user3

@pytest.fixture()
def login_user(url, setup_auth, register_user):
    _, input_data = setup_auth
    u1, u2, u3 = register_user

    data = requests.post(f"{url}/auth/login", json=input_data[0])
    assert data.status_code == 200
    user1 = data.json()
    assert user1 == u1
    
    data = requests.post(f"{url}/auth/login", json=input_data[1])
    assert data.status_code == 200
    user2 = data.json()
    assert user2 == u2
    
    data = requests.post(f"{url}/auth/login", json=input_data[2])
    assert data.status_code == 200
    user3 = data.json()
    assert user3 == u3

    return user1, user2, user3

@pytest.fixture()
def logout_user(url, login_user):
    user1, user2, user3 = login_user
    input_data = [
        {
            'token': user1['token']
        },
        {
            'token': user2['token']
        },
        {
            'token': user3['token']
        }
    ]

    data = requests.post(f"{url}/auth/logout", json=input_data[0])
    assert data.status_code == 200
    user1 = data.json()
    
    data = requests.post(f"{url}/auth/logout", json=input_data[1])
    assert data.status_code == 200
    user2 = data.json()
    
    data = requests.post(f"{url}/auth/logout", json=input_data[2])
    assert data.status_code == 200
    user3 = data.json()

    return user1['is_success'], user2['is_success'], user3['is_success']

# ---------------------------------------------------------------------------- #
''' CHANNEL FIXTURES '''

@pytest.fixture()
def setup_channel(url, setup_auth, login_user):
    user1, user2, user3 = login_user
    
    # Create a channel with the first user.
    channel_name = 'Channel_x'
    input_data = {
        'token': user1['token'],
        'name': channel_name,
        'is_public': True
    }

    data = requests.post(f"{url}/channels/create", json=input_data)
    payload = data.json()
    
    return user1, user2, user3, payload['channel_id'], channel_name

@pytest.fixture()
def invite_all_members(url, setup_channel):
    user1, user2, user3, channel_id, _ = setup_channel
    
    tok1 = user1["token"]
    uid2 = user2["u_id"]
    uid3 = user3["u_id"]

    # Make all users a member of the channel by inviting them.
    input_data = {
        'token': tok1,
        'channel_id': channel_id,
        'u_id': uid2
    }

    data = requests.get(f"{url}/channel/invite", params=input_data)
    assert data.status_code == 200
    
    input_data = {
        'token': tok1,
        'channel_id': channel_id,
        'u_id': uid3
    }

    data = requests.get(f"{url}/channel/invite", params=input_data)
    assert data.status_code == 200
