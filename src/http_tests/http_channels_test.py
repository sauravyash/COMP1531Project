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

from testing_fixtures.http_test_fixtures import url, setup_auth, setup_channels
from testing_fixtures.http_test_fixtures import register_user, login_user, logout_user

def test_url(url):
    '''Check server set up properly'''
    assert url.startswith("http")

''' ----- CHANNELS LIST ----- '''
# Test empty list (no channels)
def test_list_empty_list(url, login_user):
    user1, _, _ = login_user

    input_data = {
    	'token': user1['token']
    }

    data = requests.get(f"{url}/channels/list", params=input_data)
    assert data.status_code == 200

    assert data.json() == {
        'channels': [] 
    }

# ----- Success List
def test_list_simple(url, setup_channels):
    users, channels1, channels2, channels3 = setup_channels
    created_channel_ids = [channels1, channels2, channels3]

    # For each user, test if they can see the channels they are a member of.
    for user in users:
        input_data = {
        	'token': user['token']
        }
        data = requests.get(f"{url}/channels/list", params=input_data)
        assert data.status_code == 200
        
        channel_list = data.json()
        returned_channel_ids = [ item['channel_id'] for item in channel_list['channels'] ]
        
        index = (user['u_id'] - 1)
        assert sorted(returned_channel_ids) == sorted(created_channel_ids[index])

# ----- Fail List
def test_list_invalid_token(url, login_user):
    login_user

    input_data = {
	    'token': 'fake_token'
    }

    data = requests.get(f"{url}/channels/list", params=input_data)
    # Invalid token, raise ACCESS ERROR. (401)
    assert data.status_code == 401

def test_list_key_error(url, login_user):
    user1, _, _ = login_user

    input_data = {
	    'taken': user1['token']
    }

    data = requests.get(f"{url}/channels/list", params=input_data)
    # Bad/ Invalid input, raise KEY ERROR. (400)
    assert data.status_code == 400

''' ----- CHANNELS LISTALL ----- '''
# Test empty list (no channels)
def test_listall_empty_list(url, login_user):
    user1, _, _ = login_user

    input_data = {
	    'token': user1['token']
    }

    data = requests.get(f"{url}/channels/listall", params=input_data)

    assert data.json() == {
        'channels': [] 
    }

# ----- Success List
def test_listall_simple(url, setup_channels):
    users, channels1, channels2, channels3 = setup_channels
    created_channel_ids = channels1 + channels2 + channels3

    # For each user, test if they can see the channels they are a member of.
    for user in users:
        input_data = {
        	'token': user['token']
        }

        data = requests.get(f"{url}/channels/listall", params=input_data)
        assert data.status_code == 200

        channel_list = data.json()
        returned_channel_ids = [item['channel_id'] for item in channel_list['channels']]
        
        assert sorted(returned_channel_ids) == sorted(created_channel_ids)

# ----- Fail List
def test_listall_invalid_token(url, login_user):
    login_user
    
    input_data = {
    	'token': 'fake_token'
    }

    data = requests.get(f"{url}/channels/listall", params=input_data)
    # Invalid token, raise ACCESS ERROR. (401)
    assert data.status_code == 401

def test_listall_key_error(url, login_user):
    user1, _, _ = login_user

    input_data = {
    	'taken': user1['token']
    }

    data = requests.get(f"{url}/channels/listall", params=input_data)
    # Bad/ Invalid input, raise KEY ERROR. (400)
    assert data.status_code == 400

''' ----- CHANNELS CREATE ----- '''
# ----- Success Create
def test_create_simple(url, login_user):
    user1, _, _ = login_user
    
    # User1 creates a public channel.
    input_data = {
        'token': user1['token'],
        'name': 'channel_x',
        'is_public': True
    }

    data = requests.post(f"{url}/channels/create", json=input_data)
    ''' Checking good connection '''
    assert data.status_code == 200

    # User2 creates a private channel.
    input_data = {
        'token': user1['token'],
        'name': 'channel_x',
        'is_public': False
    }

    data = requests.post(f"{url}/channels/create", json=input_data)
    ''' Checking good connection '''
    assert data.status_code == 200

# ----- Fail Create
def test_create_invalid_channel(url, login_user):
    user1, _, _ = login_user

    input_data = {
        'token': user1["token"],
        'name': 'qwertyuiopasdfghjklzx',
        'is_public': True
    }

    data = requests.post(f"{url}/channels/create", json=input_data)
    # Invalid Channel ID, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_create_invalid_ispublic(url, login_user):
    user1, _, _ = login_user

    input_data = {
        'token': user1["token"],
        'name': 'channel_x',
        'is_public': 0
    }

    data = requests.post(f"{url}/channels/create", json=input_data)
    # Invalid is_public boolean, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_create_invalid_token(url, login_user):
    login_user

    input_data = {
        'token': 'invalid_token',
        'name': 'channel_x',
        'is_public': True
    }

    data = requests.post(f"{url}/channels/create", json=input_data)
    # Invalid token, raise ACCESS ERROR. (401)
    assert data.status_code == 401

def test_create_key_error(url, login_user):
    user1, _, _ = login_user

    input_data = {
        'taken': user1['token'],
        'name': 'channel_x',
        'is_public': True
    }

    data = requests.post(f"{url}/channels/create", json=input_data)
    # Bad/ Invalid input, raise KEY ERROR. (400)
    assert data.status_code == 400

def test_addowner_bad_request(url, login_user):
    login_user
  
    input_data = ['not', 'a', 'dictionary']
    
    data = requests.post(f"{url}/channels/create", json=input_data)
    # Bad/ Invalid input, raise BAD REQUEST ERROR. (500)
    assert data.status_code == 500

