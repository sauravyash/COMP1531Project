from subprocess import Popen, PIPE
from time import sleep
import json
import urllib
import re
import signal
import requests
import logging
import pytest

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

# Helpful Globals
EMAIL_1 = 'validemail@gmail.com'
PASSWORD_1 = 'validpassword1234'
NAME_F_1 = 'Tom'
NAME_L_1 = 'Riddles'

# ----- Clear the server, and provide details of first user.
@pytest.fixture()
def setup_auth(url):
    data = requests.delete(str(url) + "clear")
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

    input_reg = {
        'email': EMAIL_1,
        'password': PASSWORD_1,
        'name_first': NAME_F_1,
        'name_last': NAME_L_1
    }

    input_log = {
        'email': EMAIL_1,
        'password': PASSWORD_1,
    }

    return input_reg, input_log

@pytest.fixture()
def register_user(url, setup_auth):
    input_value, _ = setup_auth

    data = requests.post(str(url) + "auth/register", json=input_value)
    payload = data.json()

    return payload['token'], payload['u_id']

@pytest.fixture()
def login_user(url, setup_auth, register_user):
    _, input_data = setup_auth
    register_user

    data = requests.post(f"{url}/auth/login", json=input_data)
    payload = data.json()

    return payload['token'], payload['u_id']
