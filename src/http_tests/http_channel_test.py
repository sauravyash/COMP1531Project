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
from testing_fixtures.http_test_fixtures import setup_channel, invite_all_members

def test_url(url):
    '''Check server set up properly'''
    assert url.startswith("http")

# ---------------------------------------------------------------------------- #
''' ----- CHANNEL INVITE ----- '''

# ----- Success Invite
def test_invite_simple(url, setup_channel):
    user1, user2, user3, channel_id, _ = setup_channel

    tok1 = user1["token"]
    tok2 = user2['token']
    uid2 = user2["u_id"]
    uid3 = user3["u_id"]

    # Check that first user (owner) can add second user to channel.
    input_data = {
        'token': tok1,
        'channel_id': channel_id,
        'u_id': uid2
    }

    data = requests.post(f"{url}/channel/invite", json=input_data)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}
    
    print_data()

    # Check that second user (member) can add third user to channel.
    input_value = {
        'token': tok2,
        'channel_id': channel_id,
        'u_id': uid3
    }

    data = requests.post(f"{url}/channel/invite", json=input_value)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

# ----- Fail Invite
def test_invite_oneself(url, setup_channel):
    _, user2, _, channel_id, _ = setup_channel

    tok2 = user2['token']
    uid2 = user2["u_id"]

    input_data = {
        'token': tok2,
        'channel_id': channel_id,
        'u_id': uid2
    }

    data = requests.post(f"{url}/channel/invite", json=input_data)
    # User can't invite themself, raise ACCESS ERROR. (403)
    assert data.status_code == 403

def test_invite_invalid_token(url, setup_channel):
    _, user2, _, channel_id, _ = setup_channel

    uid2 = user2["u_id"]

    input_data = {
        'token': -99,
        'channel_id': channel_id,
        'u_id': uid2
    }

    data = requests.post(f"{url}/channel/invite", json=input_data)
    # Invalid token, raise ACCESS ERROR. (401)
    assert data.status_code == 401

def test_invite_invalid_channel(url, setup_channel):
    user1, user2, _, _, _ = setup_channel

    tok1 = user1['token']
    uid2 = user2["u_id"]

    input_data = {
        'token': tok1,
        'channel_id': -99,
        'u_id': uid2
    }

    data = requests.post(f"{url}/channel/invite", json=input_data)
    # Invalid Channel ID, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_invite_invalid_user_id(url, setup_channel):
    user1, _, _, channel_id, _ = setup_channel

    tok1 = user1["token"]

    input_data = {
        'token': tok1,
        'channel_id': channel_id,
        'u_id': -99
    }

    data = requests.post(f"{url}/channel/invite", json=input_data)
    # Invalid u_id, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_invite_key_error(url, setup_channel):
    user1, user2, _, channel_id, _ = setup_channel

    tok1 = user1["token"]
    uid2 = user2['u_id']

    input_data = {
        'taken': tok1,
        'channel_id': channel_id,
        'u_id': uid2
    }

    data = requests.post(f"{url}/channel/invite", json=input_data)
    # Bad/ Invalid input, raise KEY ERROR. (400)
    assert data.status_code == 400

def test_invite_bad_request(url, setup_channel):
    setup_channel
  
    input_data = ['not', 'a', 'dictionary']
    
    data = requests.post(f"{url}/channel/invite", json=input_data)
    # Bad/ Invalid input, raise BAD REQUEST ERROR. (500)
    assert data.status_code == 500

# ---------------------------------------------------------------------------- #
''' ----- CHANNELS DETAILS ----- '''

# ----- Success Details
def test_details_simple(url, setup_channel, invite_all_members):
    user1, user2, user3, channel_id, channel_name = setup_channel
    users = [user1, user2, user3]
    # User 1 invites all other members to the channel.
    invite_all_members

    # Check all three members can successfully view channel details.
    for user in users:
        input_data = {
            'token': user['token'],
            'channel_id': channel_id
        }

        data = requests.get(f"{url}/channel/details", params=input_data)
        ''' Checking good connection '''
        assert data.status_code == 200

        payload = data.json()
        assert payload['name'] == channel_name
        assert len(payload['owner_members']) == 1
        assert len(payload['all_members']) == 3
        assert sorted(payload['all_members']) == sorted(users)

# ----- Fail Invite
def test_details_not_member(url, setup_channel):
    _, user2, user3, channel_id, _ = setup_channel
    users = [user2, user3]

    for user in users:
        input_data = {
            'token': user['token'],
            'channel_id': channel_id
        }

        data = requests.get(f"{url}/channel/details", params=input_data)
        # User is not a member of channel, raise ACCESS ERROR. (403)
        assert data.status_code == 403

def test_details_invalid_token(url, setup_channel):
    _, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': -99,
        'channel_id': channel_id,
    }

    data = requests.get(f"{url}/channel/details", params=input_data)
    # Invalid token, raise ACCESS ERROR. (401)
    assert data.status_code == 401

def test_details_invalid_channel(url, setup_channel):
    user1, _, _, _, _ = setup_channel

    tok1 = user1['token']

    input_data = {
        'token': tok1,
        'channel_id': -99,
    }

    data = requests.get(f"{url}/channel/details", params=input_data)
    # Invalid Channel ID, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_details_key_error(url, setup_channel):
    user1, _, _, channel_id, _ = setup_channel

    tok1 = user1["token"]

    input_data = {
        'taken': tok1,
        'channel_id': channel_id,
    }

    data = requests.get(f"{url}/channel/details", params=input_data)
    # Bad/ Invalid input, raise KEY ERROR. (400)
    assert data.status_code == 400

def test_details_bad_request(url, setup_channel):
    setup_channel
  
    input_data = ['not', 'a', 'dictionary']
    
    data = requests.get(f"{url}/channel/details", params=input_data)
    # Bad/ Invalid input, raise BAD REQUEST ERROR. (500)
    assert data.status_code == 500

''' ----- CHANNELS MESSAGES ----- '''


''' ----- CHANNELS LEAVE ----- '''


''' ----- CHANNELS JOIN ----- '''


''' ----- CHANNELS ADDOWNER ----- '''


''' ----- CHANNELS REMOVEOWNER ----- '''
