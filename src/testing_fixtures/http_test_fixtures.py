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

# Helpful Globals
EMAIL_1 = 'validemail1@gmail.com'
PASSWORD_1 = 'validpassword1234'
NAME_F_1 = 'Tom'
NAME_L_1 = 'Riddles'

@pytest.fixture()
def register_user(url):
    input_value = {
        'email': EMAIL_1,
        'password': PASSWORD_1,
        'name_first': NAME_F_1,
        'name_last': NAME_L_1
    }

    data = requests.post(str(url) + "auth/register", json=input_value)
    payload = data.json()

    return payload['token'], payload['u_id']

@pytest.fixture()
def login_user(url, register_user):
    register_user

    input_value = {
        'email': EMAIL_1,
        'password': PASSWORD_1
    }

    data = requests.post(f"{url}/auth/login", json=input_value)
    payload = data.json()

    return payload['token'], payload['u_id']

