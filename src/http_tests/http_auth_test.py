############################ Http Auth Server Tests ##########################
'''
Functions to test http server auth functionality
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

from testing_fixtures.http_test_fixtures import url, setup_auth
from testing_fixtures.http_test_fixtures import register_user, login_user, logout_user

def test_url(url):
    '''Check server set up properly'''
    assert url.startswith("http")

# ---------------------------------------------------------------------------- #
''' ----- AUTH REGISTER ----- '''

# ----- Success Register
def test_reg_simple(url, setup_auth):
    input_data, _ = setup_auth
    input_data = input_data[0]

    data = requests.post(str(url) + "auth/register", json=input_data)
    # Checking good connection
    assert data.status_code == 200

    # Check return values
    payload = data.json()
    assert len(payload) == 2
    assert isinstance(payload['u_id'], int)

# ----- Fail Register
def test_reg_invalid_email(url, setup_auth):
    input_data, _ = setup_auth
    input_data = input_data[0]
    
    input_data['email'] = 'invalidemail'
    data = requests.post(str(url) + "auth/register", json=input_data)
    # Invalid email, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_reg_invalid_password(url, setup_auth):
    input_data, _ = setup_auth
    input_data = input_data[0]
    
    input_data['password'] = '123'
    data = requests.post(str(url) + "auth/register", json=input_data)
    # Invalid password, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_reg_empty_password(url, setup_auth):
    input_data, _ = setup_auth
    input_data = input_data[0]
    
    input_data['password'] = ''
    data = requests.post(str(url) + "auth/register", json=input_data)
    # Empty password, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_reg_invalid_fname(url, setup_auth):
    input_data, _ = setup_auth
    input_data = input_data[0]
    
    input_data['name_first'] = 'invalidfirstnamewhichisgoingtobemorethan50characterslong'
    data = requests.post(str(url) + "auth/register", json=input_data)
    # Invalid first name, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_reg_invalid_lname(url, setup_auth):
    input_data, _ = setup_auth
    input_data = input_data[0]
    
    input_data['name_last'] = 'invalidlastnamewhichisgoingtobemorethan50characterslong'
    data = requests.post(str(url) + "auth/register", json=input_data)
    # Invalid last name, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_reg_empty_first_name(url, setup_auth):
    input_data, _ = setup_auth
    input_data = input_data[0]
    
    input_data['name_first'] = ''
    data = requests.post(str(url) + "auth/register", json=input_data)
    # Empty first name, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_reg_empty_last_name(url, setup_auth):
    input_data, _ = setup_auth
    input_data = input_data[0]
    
    input_data['name_last'] = ''
    data = requests.post(str(url) + "auth/register", json=input_data)
    # Empty last name, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_already_registered(url, setup_auth, register_user):
    input_data, _ = setup_auth
    input_data = input_data[0]
    # Register user once.
    register_user

    # Register user again
    data = requests.post(str(url) + "auth/register", json=input_data)
    # User can not be registered again, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_reg_key_error(url):
    setup_auth
    input_data = {
        'emale': 'validemail@gmail.com',
        'password': 'validpassword1234',
        'name_f': 'Harry',
        'name_last': 'Harrison'
    }
    
    data = requests.post(str(url) + "auth/register", json=input_data)
    # Bad/ Invalid input, raise KEY ERROR. (400)
    assert data.status_code == 400

def test_reg_bad_request(url):
    setup_auth
    input_data = ['not', 'a', 'dictionary']
    
    data = requests.post(str(url) + "auth/register", json=input_data)
    # Bad/ Invalid input, raise BAD REQUEST ERROR. (500)
    assert data.status_code == 500

# ---------------------------------------------------------------------------- #
''' ----- AUTH LOGIN ----- '''

# ----- Success Login
def test_login_simple(url, setup_auth, register_user):
    _, input_data = setup_auth
    input_data = input_data[0]
    user1, _, _ = register_user

    data = requests.post(f"{url}/auth/login", json=input_data)

    # Checking good connection
    assert data.status_code == 200

    # Check return values
    payload = data.json()
    assert len(payload) == 2
    assert payload['token'] == user1['token']
    assert payload['u_id'] == user1['u_id']

# ----- Fail Login
def test_login_unregistered_email(url, setup_auth):
    _, input_data = setup_auth
    input_data = input_data[0]
    
    data = requests.post(f"{url}/auth/login", json=input_data)
    # Email has not been registered, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_login_incorrect_password(url, setup_auth, register_user):
    _, input_data = setup_auth
    input_data = input_data[0]
    register_user

    input_data['password'] = 'incorrect_password'
    data = requests.post(f"{url}/auth/login", json=input_data)
    # Incorrect password, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_login_invalid_email(url, setup_auth, register_user):
    _, input_data = setup_auth
    input_data = input_data[0]
    register_user

    input_data['email'] = 'invalidemail'
    data = requests.post(str(url) + "auth/login", json=input_data)
    # Invalid email, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_login_empty_email(url, setup_auth, register_user):
    _, input_data = setup_auth
    input_data = input_data[0]
    register_user

    input_data['email'] = ''
    data = requests.post(str(url) + "auth/login", json=input_data)
    # Empty email, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_login_empty_password(url, setup_auth, register_user):
    _, input_data = setup_auth
    input_data = input_data[0]
    register_user

    input_data['password'] = ''
    data = requests.post(str(url) + "auth/login", json=input_data)
    # Invalid email, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_login_key_error(url, setup_auth):
    setup_auth
    input_data = {
        'emale': 'validemail@gmail.com',
        'password': 'validpassword1234',
    }
    
    data = requests.post(str(url) + "auth/login", json=input_data)
    # Bad/ Invalid input, raise KEY ERROR. (400)
    assert data.status_code == 400

def test_login_bad_request(url, setup_auth):
    setup_auth
    input_data = ['not', 'a', 'dictionary']
    
    data = requests.post(str(url) + "auth/login", json=input_data)
    # Bad/ Invalid input, raise BAD REQUEST ERROR. (500)
    assert data.status_code == 500

# ---------------------------------------------------------------------------- #
''' ----- AUTH LOGOUT ----- '''

# ----- Success Logout
def test_logout_simple(url, login_user):
    user1, _, _ = login_user

    input_data = {
        'token': user1['token']
    }

    data = requests.post(f"{url}/auth/logout", json=input_data)
    
    # Checking good connection
    assert data.status_code == 200

    # Check return values
    payload = data.json()
    assert payload['is_success'] is True

# ----- Fail Logout
def test_already_logged_out(url, login_user, logout_user):
    user1, _, _ = login_user
    logout_result, _, _ = logout_user
    assert logout_result == True

    input_data = {
        'token': user1['token']
    }

    data = requests.post(f"{url}/auth/logout", json=input_data)
    payload = data.json()
    # Already logged out, logout FAILS.
    assert payload['is_success'] is False

def test_logout_invalid_token(url, login_user):
    login_user

    input_data = {
        'token': -99
    }

    data = requests.post(f"{url}/auth/logout", json=input_data)
    # Invalid token, raise ACCESS ERROR. (401)
    assert data.status_code == 401

def test_logout_key_error(url, login_user):
    user1, _, _ = login_user
    input_data = {
        'taken': user1['token']
    }
    
    data = requests.post(str(url) + "auth/logout", json=input_data)
    # Bad/ Invalid input, raise KEY ERROR. (400)
    assert data.status_code == 400

def test_logout_bad_request(url, login_user):
    login_user
    input_data = ['not', 'a', 'dictionary']
    
    data = requests.post(str(url) + "auth/logout", json=input_data)
    # Bad/ Invalid input, raise BAD REQUEST ERROR. (500)
    assert data.status_code == 500
