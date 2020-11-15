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

from testing_fixtures.http_test_fixtures import url, setup_auth, setup_channel
from testing_fixtures.http_test_fixtures import register_user, login_user, logout_user
from testing_fixtures.http_test_fixtures import invite_all_members, all_members_owners

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
''' ----- CHANNEL DETAILS ----- '''

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

''' ----- CHANNEL MESSAGES ----- '''

# ----- Success Messages
def test_messages_simple(url, setup_channel):
    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'start': 0
    }

    data = requests.get(f"{url}/channel/messages", params=input_data)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {
        "messages": [],
        "start": 0,
        "end": -1,
    }

# ----- Fail Messages
def test_messages_not_member(url, setup_channel):
    _, user2, _, channel_id, _ = setup_channel

    input_data = {
        'token': user2["token"],
        'channel_id': channel_id,
        'start': 0
    }

    data = requests.get(f"{url}/channel/messages", params=input_data)
    # User is not a member of channel, raise ACCESS ERROR. (403)
    assert data.status_code == 403


def test_messages_invalid_channel(url, setup_channel):
    user1, _, _, _, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': -99,
        'start': 0
    }

    data = requests.get(f"{url}/channel/messages", params=input_data)
    # Invalid Channel ID, raise INPUT ERROR. (401)
    assert data.status_code == 401


def test_messages_invalid_start(url, setup_channel):
    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'start': -99
    }

    data = requests.get(f"{url}/channel/messages", params=input_data)
    # Invalid Channel ID, raise INPUT ERROR. (401)
    assert data.status_code == 401


def test_messages_invalid_token(url, setup_channel):
    _, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': 'invalid_token',
        'channel_id': channel_id,
        'start': 0
    }

    data = requests.get(f"{url}/channel/messages", params=input_data)
    # Invalid token, raise ACCESS ERROR. (401)
    assert data.status_code == 401

def test_messages_key_error(url, setup_channel):
    user1, _, _, channel_id, _ = setup_channel

    tok1 = user1["token"]

    input_data = {
        'taken': tok1,
        'channel_id': channel_id,
        'start': 0
    }

    data = requests.get(f"{url}/channel/messages", params=input_data)
    # Bad/ Invalid input, raise KEY ERROR. (400)
    assert data.status_code == 400

''' ----- CHANNEL LEAVE ----- '''
# ----- Success Leave
def test_leave_simple(url, setup_channel, invite_all_members):
    user1, user2, _, channel_id, _ = setup_channel
    invite_all_members

    # A member leaves the channel.
    input_data = {
        'token': user2['token'],
        'channel_id': channel_id
    }

    data = requests.post(f"{url}/channel/leave", json=input_data)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

    # An owner leaves the channel.
    input_data = {
        'token': user1['token'],
        'channel_id': channel_id
    }

    data = requests.post(f"{url}/channel/leave", json=input_data)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

# ----- Fail Leave
def test_leave_not_member(url, setup_channel):
    _, user2, _, channel_id, _ = setup_channel

    input_data = {
        'token': user2["token"],
        'channel_id': channel_id
    }

    data = requests.post(f"{url}/channel/leave", json=input_data)
    # User is not a member of channel, raise ACCESS ERROR. (403)
    assert data.status_code == 403


def test_leave_invalid_channel(url, setup_channel):
    user1, _, _, _, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': -99
    }

    data = requests.post(f"{url}/channel/leave", json=input_data)
    # Invalid Channel ID, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_leave_invalid_token(url, setup_channel):
    _, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': 'invalid_token',
        'channel_id': channel_id
    }

    data = requests.post(f"{url}/channel/leave", json=input_data)
    # Invalid token, raise ACCESS ERROR. (401)
    assert data.status_code == 401

def test_leave_key_error(url, setup_channel):
    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'taken': user1['token'],
        'channel_id': channel_id
    }

    data = requests.post(f"{url}/channel/leave", json=input_data)
    # Bad/ Invalid input, raise KEY ERROR. (400)
    assert data.status_code == 400

def test_leave_bad_request(url, setup_channel):
    setup_channel

    input_data = ['not', 'a', 'dictionary']

    data = requests.post(f"{url}/channel/leave", json=input_data)
    # Bad/ Invalid input, raise BAD REQUEST ERROR. (500)
    assert data.status_code == 500

''' ----- CHANNEL JOIN ----- '''

# ----- Success Join
def test_join_simple(url, setup_channel):
    _, user2, _, channel_id, _ = setup_channel

    # A member joins the channel.
    input_data = {
        'token': user2['token'],
        'channel_id': channel_id
    }

    data = requests.post(f"{url}/channel/join", json=input_data)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

# ----- Fail Join
def test_join_private(url, setup_channel):
    user1, user2, _, _, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'name': 'Channel_x',
        'is_public': False
    }

    data = requests.post(f"{url}/channels/create", json=input_data)
    assert data.status_code == 200

    payload = data.json()
    channel_id = payload['channel_id']

    input_data = {
        'token': user2['token'],
        'channel_id': channel_id
    }

    data = requests.post(f"{url}/channel/join", json=input_data)
    # User can not join private channel, raise ACCESS ERROR. (403)
    assert data.status_code == 403

def test_join_invalid_channel(url, setup_channel):
    user1, _, _, _, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': -99
    }

    data = requests.post(f"{url}/channel/join", json=input_data)
    # Invalid Channel ID, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_join_invalid_token(url, setup_channel):
    _, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': 'invalid_token',
        'channel_id': channel_id
    }

    data = requests.post(f"{url}/channel/join", json=input_data)
    # Invalid token, raise ACCESS ERROR. (401)
    assert data.status_code == 401

def test_join_key_error(url, setup_channel):
    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'taken': user1['token'],
        'channel_id': channel_id
    }

    data = requests.post(f"{url}/channel/join", json=input_data)
    # Bad/ Invalid input, raise KEY ERROR. (400)
    assert data.status_code == 400

def test_join_bad_request(url, setup_channel):
    setup_channel

    input_data = ['not', 'a', 'dictionary']

    data = requests.post(f"{url}/channel/join", json=input_data)
    # Bad/ Invalid input, raise BAD REQUEST ERROR. (500)
    assert data.status_code == 500

''' ----- CHANNEL ADDOWNER ----- '''

# ----- Success Addowner
def test_addowner_simple(url, setup_channel, invite_all_members):
    user1, user2, _, channel_id, _ = setup_channel
    invite_all_members

    # A member joins the channel.
    input_data = {
        'token': user1['token'],
        'channel_id': channel_id,
        'u_id': user2['u_id']
    }

    data = requests.post(f"{url}/channel/addowner", json=input_data)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

# ----- Fail Addowner
def test_addowner_not_auth(url, setup_channel, invite_all_members):
    _, user2, user3, channel_id, _ = setup_channel
    invite_all_members

    input_data = {
        'token': user2["token"],
        'channel_id': channel_id,
        'u_id': user3['u_id']
    }

    data = requests.post(f"{url}/channel/addowner", json=input_data)
    # User is not an owner, raise ACCESS ERROR. (403)
    assert data.status_code == 403

def test_addowner_already_owner(url, setup_channel, invite_all_members):
    user1, user2, _, channel_id, _ = setup_channel
    invite_all_members

    # Firstly make user2 an owner.
    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'u_id': user2['u_id']
    }

    data = requests.post(f"{url}/channel/addowner", json=input_data)
    assert data.status_code == 200

    input_data = {
        'token': user2["token"],
        'channel_id': channel_id,
        'u_id': user1['u_id']
    }

    data = requests.post(f"{url}/channel/addowner", json=input_data)
    # User is already an owner, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_addowner_invalid_channel(url, setup_channel, invite_all_members):
    user1, user2, _, _, _ = setup_channel
    invite_all_members

    input_data = {
        'token': user1["token"],
        'channel_id': -99,
        'u_id': user2['u_id']
    }

    data = requests.post(f"{url}/channel/addowner", json=input_data)
    # Invalid Channel ID, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_addowner_invalid_token(url, setup_channel, invite_all_members):
    _, user2, _, channel_id, _ = setup_channel
    invite_all_members

    input_data = {
        'token': 'invalid_token',
        'channel_id': channel_id,
        'u_id': user2['u_id']
    }

    data = requests.post(f"{url}/channel/addowner", json=input_data)
    # Invalid token, raise ACCESS ERROR. (401)
    assert data.status_code == 401

def test_addowner_key_error(url, setup_channel, invite_all_members):
    user1, user2, _, channel_id, _ = setup_channel
    invite_all_members

    input_data = {
        'taken': user1['token'],
        'channel_id': channel_id,
        'u_id': user2['u_id']
    }

    data = requests.post(f"{url}/channel/addowner", json=input_data)
    # Bad/ Invalid input, raise KEY ERROR. (400)
    assert data.status_code == 400

def test_addowner_bad_request(url, setup_channel):
    setup_channel

    input_data = ['not', 'a', 'dictionary']

    data = requests.post(f"{url}/channel/addowner", json=input_data)
    # Bad/ Invalid input, raise BAD REQUEST ERROR. (500)
    assert data.status_code == 500

''' ----- CHANNEL REMOVEOWNER ----- '''

# ----- Success Removeowner
def test_removeowner_simple(url, setup_channel, all_members_owners):
    user1, user2, _, channel_id, _ = setup_channel
    all_members_owners

    # User1 removes User2 as an owner.
    input_data = {
        'token': user1['token'],
        'channel_id': channel_id,
        'u_id': user2['u_id']
    }

    data = requests.post(f"{url}/channel/removeowner", json=input_data)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

# ----- Fail Removeowner
def test_removeowner_not_auth(url, setup_channel, invite_all_members):
    user1, user2, _, channel_id, _ = setup_channel
    invite_all_members

    input_data = {
        'token': user2["token"],
        'channel_id': channel_id,
        'u_id': user1['u_id']
    }

    data = requests.post(f"{url}/channel/addowner", json=input_data)
    # User is not an owner, raise ACCESS ERROR. (403)
    assert data.status_code == 403

def test_removeowner_member(url, setup_channel, invite_all_members):
    user1, user2, _, channel_id, _ = setup_channel
    invite_all_members

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'u_id': user2['u_id']
    }

    data = requests.post(f"{url}/channel/removeowner", json=input_data)
    # User is already an owner, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_removeowner_invalid_channel(url, setup_channel, all_members_owners):
    user1, user2, _, _, _ = setup_channel
    all_members_owners

    input_data = {
        'token': user1["token"],
        'channel_id': -99,
        'u_id': user2['u_id']
    }

    data = requests.post(f"{url}/channel/removeowner", json=input_data)
    # Invalid Channel ID, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_removeowner_invalid_token(url, setup_channel, all_members_owners):
    _, user2, _, channel_id, _ = setup_channel
    all_members_owners

    input_data = {
        'token': 'invalid_token',
        'channel_id': channel_id,
        'u_id': user2['u_id']
    }

    data = requests.post(f"{url}/channel/removeowner", json=input_data)
    # Invalid token, raise ACCESS ERROR. (401)
    assert data.status_code == 401

def test_removeowner_key_error(url, setup_channel, invite_all_members):
    user1, user2, _, channel_id, _ = setup_channel
    all_members_owners

    input_data = {
        'taken': user1['token'],
        'channel_id': channel_id,
        'u_id': user2['u_id']
    }

    data = requests.post(f"{url}/channel/removeowner", json=input_data)
    # Bad/ Invalid input, raise KEY ERROR. (400)
    assert data.status_code == 400

def test_removeowner_bad_request(url, setup_channel):
    setup_channel

    input_data = ['not', 'a', 'dictionary']

    data = requests.post(f"{url}/channel/removeowner", json=input_data)
    # Bad/ Invalid input, raise BAD REQUEST ERROR. (500)
    assert data.status_code == 500
