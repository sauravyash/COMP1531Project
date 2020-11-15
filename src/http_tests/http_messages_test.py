'''
Functions to test http server message functionality
'''

from subprocess import Popen, PIPE
from time import sleep
import string
import random
import json
import urllib
import re
import signal
import requests
import logging
import pytest
import datetime as dt

from data import print_data

from testing_fixtures.http_test_fixtures import url, setup_auth, setup_channel
from testing_fixtures.http_test_fixtures import register_user, login_user, logout_user
from testing_fixtures.http_test_fixtures import invite_all_members, all_members_owners

def test_url(url):
    '''Check server set up properly'''
    assert url.startswith("http")

# ---------------------------------------------------------------------------- #
''' ----- MESSAGES ----- '''

# ----- Success

def test_message_sucess_send(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    data = requests.post(f"{url}/message/send", json=input_data)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert isinstance(payload['message_id'], int)

def test_message_fail_send_not_member(url, setup_channel):

    _, user2, _, channel_id, _ = setup_channel

    input_data = {
        'token': user2["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    data = requests.post(f"{url}/message/send", json=input_data)
    # User is not a member of channel, raise ACCESS ERROR. (403)
    assert data.status_code == 403

def test_message_fail_send_exceeds_word_limit(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel

    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(1005))

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': result_str
    }

    data = requests.post(f"{url}/message/send", json=input_data)
    # Exceeds Word Limit, raise INPUT ERROR. (401)
    assert data.status_code == 401


def test_message_success_sendlater(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel
    send_time = (dt.datetime.now() + dt.timedelta(hours=10)).timestamp()

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello',
        'time_sent': send_time
    }

    data = requests.post(f"{url}/message/sendlater", json=input_data)
    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert isinstance(payload['message_id'], int)

def test_message_fail_sendlater_exceeds_word_limit(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel

    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(1005))
    send_time = (dt.datetime.now() + dt.timedelta(hours=10)).timestamp()

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': result_str,
        'time_sent': send_time
    }

    data = requests.post(f"{url}/message/sendlater", json=input_data)
    # Exceeds Word Limit, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_message_fail_sendlater_invalidtime(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel
    send_time = dt.datetime(2000, 9, 11, 8, 0).timestamp()

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello',
        'time_sent': send_time
    }

    data = requests.post(f"{url}/message/sendlater", json=input_data)
    # Input Error, raise INPUT ERROR. (401)
    assert data.status_code == 401

def test_message_fail_sendlater_not_member(url, setup_channel):

    _, user2, _, channel_id, _ = setup_channel
    send_time = (dt.datetime.now() + dt.timedelta(hours=10)).timestamp()

    input_data = {
        'token': user2["token"],
        'channel_id': channel_id,
        'message': 'hello',
        'time_sent': send_time
    }

    data = requests.post(f"{url}/message/sendlater", json=input_data)
    # User is not a member of channel, raise ACCESS ERROR. (403)
    assert data.status_code == 403

def test_message_fail_send_later_invalid_channel(url, setup_channel):

    user1, _, _, _, _ = setup_channel
    send_time = (dt.datetime.now() + dt.timedelta(hours=10)).timestamp()
    input_data = {
        'token': user1["token"],
        'channel_id': -99,
        'message': 'hello',
        'time_sent': send_time
    }

    data = requests.post(f"{url}/message/sendlater", json=input_data)
    # Invalid Channel ID, raise INPUT ERROR. (401)
    assert data.status_code == 401


def test_message_success_edit(url, setup_channel):
        user1, _, _, channel_id, _ = setup_channel

        input_data = {
            'token': user1["token"],
            'channel_id': channel_id,
            'message': 'hello'
        }

        data = requests.post(f"{url}/message/send", json=input_data)
        payload = data.json()
        message_1 = payload['message_id']

        ''' Checking good connection '''
        assert data.status_code == 200

        input_data = {
            'token': user1["token"],
            'message_id': message_1,
            'message': 'hi'
        }

        data = requests.put(f"{url}/message/edit", json=input_data)

        ''' Checking good connection '''
        assert data.status_code == 200

        payload = data.json()
        assert payload == {}

def test_message_fail_edit_unauthorised_user(url, setup_channel):

    user1, user2, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    data = requests.post(f"{url}/message/send", json=input_data)
    payload = data.json()
    message_1 = payload['message_id']

    ''' Checking good connection '''
    assert data.status_code == 200

    input_data = {
        'token': user2["token"],
        'message_id': message_1,
        'message': 'hi'
    }

    data = requests.put(f"{url}/message/edit", json=input_data)

    # Not Authorised User, raise ACCESS ERROR. (403)
    assert data.status_code == 403

def test_message_success_remove(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }


    data = requests.post(f"{url}/message/send", json=input_data)
    payload = data.json()
    message_1 = payload['message_id']

    input_data = {
        'token': user1["token"],
        'message_id': message_1
    }

    data = requests.delete(f"{url}/message/remove", json=input_data)

    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

def test_message_fail_remove(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    requests.post(f"{url}/message/send", json=input_data)

    input_data = {
        'token': user1["token"],
        'message_id': -99
    }

    data = requests.delete(f"{url}/message/remove", json=input_data)

    # Invalid message ID. raise Input Error (401)
    assert data.status_code == 401

def test_message_fail_remove_unauthorised_user(url, setup_channel):

    user1, user2, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    data = requests.post(f"{url}/message/send", json=input_data)
    payload = data.json()
    message_1 = payload['message_id']

    ''' Checking good connection '''
    assert data.status_code == 200

    input_data = {
        'token': user2["token"],
        'message_id': message_1,
    }

    data = requests.delete(f"{url}/message/remove", json=input_data)

    # Not Authorised User, raise ACCESS ERROR. (403)
    assert data.status_code == 403

def test_message_success_react(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    data = requests.post(f"{url}/message/send", json=input_data)
    payload = data.json()
    message_1 = payload['message_id']

    input_data = {
        'token': user1["token"],
        'message_id': message_1,
        'react_id': 1
    }

    data = requests.post(f"{url}/message/react", json=input_data)

    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

def test_message_fail_react_invalid_react_id(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    data = requests.post(f"{url}/message/send", json=input_data)
    payload = data.json()
    message_1 = payload['message_id']

    input_data = {
        'token': user1["token"],
        'message_id': message_1,
        'react_id': -99
    }

    data = requests.post(f"{url}/message/react", json=input_data)

    # Invalid react ID. raise Input Error (401)
    assert data.status_code == 401

def test_message_fail_react_invalid_message_id(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    requests.post(f"{url}/message/send", json=input_data)

    input_data = {
        'token': user1["token"],
        'message_id': 999,
        'react_id': 1
    }

    data = requests.post(f"{url}/message/react", json=input_data)

    # Invalid message ID. raise Input Error (401)
    assert data.status_code == 401

def test_message_fail_react_already_reacted(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    data = requests.post(f"{url}/message/send", json=input_data)
    payload = data.json()
    message_1 = payload['message_id']

    input_data = {
        'token': user1["token"],
        'message_id': message_1,
        'react_id': 1
    }

    requests.post(f"{url}/message/react", json=input_data)
    data = requests.post(f"{url}/message/react", json=input_data)

    # Already reacted. raise Input Error (401)
    assert data.status_code == 401

def test_message_sucess_unreact(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    data = requests.post(f"{url}/message/send", json=input_data)
    payload = data.json()
    message_1 = payload['message_id']

    input_data = {
        'token': user1["token"],
        'message_id': message_1,
        'react_id': 1
    }

    requests.post(f"{url}/message/react", json=input_data)
    data = requests.post(f"{url}/message/unreact", json=input_data)


    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

def test_message_fail_unreact_invalid_message_id(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    data = requests.post(f"{url}/message/send", json=input_data)
    payload = data.json()
    message_1 = payload['message_id']

    input_data = {
        'token': user1["token"],
        'message_id': message_1,
        'react_id': 1
    }

    requests.post(f"{url}/message/react", json=input_data)

    input_data = {
        'token': user1["token"],
        'message_id': -99,
        'react_id': 1
    }

    data = requests.post(f"{url}/message/unreact", json=input_data)

    # Invalid message ID. raise Input Error (401)
    assert data.status_code == 401

def test_message_fail_unreact_invalid_react_id(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    data = requests.post(f"{url}/message/send", json=input_data)
    payload = data.json()
    message_1 = payload['message_id']

    input_data = {
        'token': user1["token"],
        'message_id': message_1,
        'react_id': 1
    }

    requests.post(f"{url}/message/react", json=input_data)

    input_data = {
        'token': user1["token"],
        'message_id': message_1,
        'react_id': -99
    }

    data = requests.post(f"{url}/message/unreact", json=input_data)

    # Invalid message ID. raise Input Error (401)
    assert data.status_code == 401

def test_message_fail_unreact_twice(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    data = requests.post(f"{url}/message/send", json=input_data)
    payload = data.json()
    message_1 = payload['message_id']

    input_data = {
        'token': user1["token"],
        'message_id': message_1,
        'react_id': 1
    }

    requests.post(f"{url}/message/react", json=input_data)

    input_data = {
        'token': user1["token"],
        'message_id': message_1,
        'react_id': 1
    }

    requests.post(f"{url}/message/unreact", json=input_data)
    data = requests.post(f"{url}/message/unreact", json=input_data)

    # Invalid message ID. raise Input Error (401)
    assert data.status_code == 401

def test_message_sucess_pin(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    data = requests.post(f"{url}/message/send", json=input_data)
    payload = data.json()
    message_1 = payload['message_id']

    input_data = {
        'token': user1["token"],
        'message_id': message_1,
        'is_pinned': True
    }

    data = requests.post(f"{url}/message/pin", json=input_data)

    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

def test_message_fail_pin_invalid_message_id(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    requests.post(f"{url}/message/send", json=input_data)

    input_data = {
        'token': user1["token"],
        'message_id': -99,
        'is_pinned': True
    }

    data = requests.post(f"{url}/message/pin", json=input_data)

    # Invalid message ID. raise Input Error (401)
    assert data.status_code == 401

def test_message_fail_pin_already_pinned(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    data = requests.post(f"{url}/message/send", json=input_data)
    payload = data.json()
    message_1 = payload['message_id']

    input_data = {
        'token': user1["token"],
        'message_id': message_1,
        'is_pinned': True
    }

    requests.post(f"{url}/message/pin", json=input_data)
    data = requests.post(f"{url}/message/pin", json=input_data)

    # Invalid message ID. raise Input Error (401)
    assert data.status_code == 401

def test_message_fail_pin_not_authorised(url, setup_channel):

    user1, user2, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    data = requests.post(f"{url}/message/send", json=input_data)
    payload = data.json()
    message_1 = payload['message_id']

    ''' Checking good connection '''
    assert data.status_code == 200

    input_data = {
        'token': user2["token"],
        'message_id': message_1,
        'is_pinned': True
    }

    data = requests.post(f"{url}/message/pin", json=input_data)

    # Not Authorised User, raise ACCESS ERROR. (403)
    assert data.status_code == 403

def test_message_sucess_unpin(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    data = requests.post(f"{url}/message/send", json=input_data)
    payload = data.json()
    message_1 = payload['message_id']

    input_data = {
        'token': user1["token"],
        'message_id': message_1,
        'is_pinned': True
    }

    requests.post(f"{url}/message/pin", json=input_data)
    data = requests.post(f"{url}/message/unpin", json=input_data)

    ''' Checking good connection '''
    assert data.status_code == 200

    payload = data.json()
    assert payload == {}

def test_message_fail_unpin_invalid_message_id(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    data = requests.post(f"{url}/message/send", json=input_data)
    payload = data.json()
    message_1 = payload['message_id']

    input_data = {
        'token': user1["token"],
        'message_id': message_1,
        'is_pinned': True
    }

    requests.post(f"{url}/message/pin", json=input_data)

    input_data = {
        'token': user1["token"],
        'message_id': -99,
        'is_pinned': True
    }

    data = requests.post(f"{url}/message/unpin", json=input_data)

    # Invalid message ID. raise Input Error (401)
    assert data.status_code == 401

def test_message_fail_already_unpinned(url, setup_channel):

    user1, _, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    data = requests.post(f"{url}/message/send", json=input_data)
    payload = data.json()
    message_1 = payload['message_id']

    input_data = {
        'token': user1["token"],
        'message_id': message_1,
        'is_pinned': True
    }

    requests.post(f"{url}/message/pin", json=input_data)
    requests.post(f"{url}/message/unpin", json=input_data)
    data = requests.post(f"{url}/message/unpin", json=input_data)

    # Not Authorised User, raise ACCESS ERROR. (401)
    assert data.status_code == 401

def test_message_fail_unpin_not_authorised(url, setup_channel):

    user1, user2, _, channel_id, _ = setup_channel

    input_data = {
        'token': user1["token"],
        'channel_id': channel_id,
        'message': 'hello'
    }

    data = requests.post(f"{url}/message/send", json=input_data)
    payload = data.json()
    message_1 = payload['message_id']

    ''' Checking good connection '''
    assert data.status_code == 200

    input_data = {
        'token': user1["token"],
        'message_id': message_1,
        'is_pinned': True
    }

    requests.post(f"{url}/message/pin", json=input_data)

    input_data = {
        'token': user2["token"],
        'message_id': message_1,
        'is_pinned': True
    }

    data =requests.post(f"{url}/message/unpin", json=input_data)

    # Not Authorised User, raise ACCESS ERROR. (403)
    assert data.status_code == 403
