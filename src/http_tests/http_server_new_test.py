############################ Http Server Tests ##########################
'''
Functions to test http server functionality
'''

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

import testing_fixtures.http_test_fixtures
from testing_fixtures.http_test_fixtures import url
from testing_fixtures.http_test_fixtures import setup_auth
from testing_fixtures.http_test_fixtures import register_user
from testing_fixtures.http_test_fixtures import login_user

def test_url(url):
    '''Check server set up properly'''
    assert url.startswith("http")

''' ----- AUTH TESTS ----- '''
# ---------------------------------------------------------------------------- #

''' ----- AUTH REGISTER ----- '''
# ----- Success Register
def test_register_simple(url, setup_auth):
    input_data = setup_auth

    data = requests.post(str(url) + "auth/register", json=input_data)
    # Checking good connection
    assert data.status_code == 200

    # Check return values
    payload = data.json()
    assert len(payload) == 2
    assert isinstance(payload['u_id'], int)

# ----- Fail Register
def test_invalid_email(url, setup_auth):
    input_data = setup_auth
    
    input_data['email'] = 'invalidemail'
    data = requests.post(str(url) + "auth/register", json=input_data)
    # Invalid email, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_invalid_password(url, setup_auth):
    input_data = setup_auth
    
    input_data['password'] = '123'
    data = requests.post(str(url) + "auth/register", json=input_data)
    # Invalid password, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_empty_password(url, setup_auth):
    input_data = setup_auth
    
    input_data['password'] = ''
    data = requests.post(str(url) + "auth/register", json=input_data)
    # Empty password, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_invalid_fname(url, setup_auth):
    input_data = setup_auth
    
    input_data['name_first'] = 'invalidfirstnamewhichisgoingtobemorethan50characterslong'
    data = requests.post(str(url) + "auth/register", json=input_data)
    # Invalid first name, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_invalid_lname(url, setup_auth):
    input_data = setup_auth
    
    input_data['name_last'] = 'invalidlastnamewhichisgoingtobemorethan50characterslong'
    data = requests.post(str(url) + "auth/register", json=input_data)
    # Invalid last name, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_empty_first_name(url, setup_auth):
    input_data = setup_auth
    
    input_data['name_first'] = ''
    data = requests.post(str(url) + "auth/register", json=input_data)
    # Empty first name, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_empty_last_name(url, setup_auth):
    input_data = setup_auth
    
    input_data['name_last'] = ''
    data = requests.post(str(url) + "auth/register", json=input_data)
    # Empty last name, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_already_registered(url, setup_auth, register_user):
    input_data = setup_auth
    # Register user once.
    register_user

    # Register user again
    data = requests.post(str(url) + "auth/register", json=input_data)
    # User can not be registered again, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_key_error(url):
    input_data = {
        'emale': 'validemail@gmail.com',
        'password': 'validpassword1234',
        'name_f': 'Harry',
        'name_last': 'Harrison'
    }
    
    data = requests.post(str(url) + "auth/register", json=input_data)
    # Bad/ Invalid input, raise KEY ERROR. (400)
    assert data.status_code == 400

def test_bad_request(url):
    input_data = ['not', 'a', 'dictionary']
    
    data = requests.post(str(url) + "auth/register", json=input_data)
    # Bad/ Invalid input, raise BAD REQUEST ERROR. (500)
    assert data.status_code == 500

''' ----- AUTH LOGIN ----- '''
def test_login_simple(url, setup_auth, register_user):
    input_data = setup_auth
    tok1, uid1 = register_user
    
    input_value = {
        'email': input_data['email'],
        'password': input_data['password']
    }

    data = requests.post(f"{url}/auth/login", json=input_value)

    # Checking good connection
    assert data.status_code == 200

    # Check return values
    payload = data.json()
    assert len(payload) == 2
    assert payload['token'] == tok1
    assert payload['u_id'] == uid1

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

