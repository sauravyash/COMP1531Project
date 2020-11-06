############################ Http Server Tests ##########################
'''
Functions to test http server functionality
'''

import pytest

from subprocess import Popen, PIPE
from time import sleep
import json
import urllib
import re
import signal
import requests
import logging

from data import print_data

from testing_fixtures.http_test_fixtures import url
from testing_fixtures.http_test_fixtures import register_user
from testing_fixtures.http_test_fixtures import login_user

EMAIL_1 = 'validemail1@gmail.com'
PASSWORD_1 = 'validpassword1234'
NAME_F_1 = 'Tom'
NAME_L_1 = 'Riddles'

def test_url(url):
    '''Check server set up properly'''
    assert url.startswith("http")

# AUTH TESTS
# ---------------------------------------------------------------------------- #

''' ----- AUTH REGISTER ----- '''
def test_register_simple(url):
    
    input_value = {
        'email': EMAIL_1,
        'password': PASSWORD_1,
        'name_first': NAME_F_1,
        'name_last': NAME_L_1
    }

    data = requests.post(str(url) + "auth/register", json=input_value)

    # Checking good connection
    assert data.status_code == 200

    # Check return values
    payload = data.json()
    assert len(payload) == 2
    assert isinstance(payload['u_id'], int)

# Add tests for all invalid cases...

''' ----- AUTH LOGIN ----- '''
def test_login_simple(url, register_user):
    
    tok1, uid1 = register_user
    
    input_value = {
        'email': EMAIL_1,
        'password': PASSWORD_1
    }

    data = requests.post(f"{url}/auth/login", json=input_value)

    # Checking good connection
    assert data.status_code == 200

    # Check return values
    payload = data.json()
    assert len(payload) == 2
    assert payload['token'] == tok1
    assert payload['u_id'] == uid1

# Add tests for all invalid cases...

''' ----- LOGOUT USER1 ----- '''
def test_logout_simple(url, login_user):
    tok1, _ = login_user

    input_value = {
        'token': tok1
    }

    data = requests.post(f"{url}/auth/logout", json=input_value)
    
    # Checking good connection
    assert data.status_code == 200

    # Check return values
    payload = data.json()
    assert payload['is_success'] is True

# Add tests for all invalid cases...

