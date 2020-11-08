############################## Standup Send Tests ############################
'''
Functions to test standup_send functionality
'''

''' NOT YET IMPLEMENTED
import pytest
import other
import string
import random

from error import InputError, AccessError
from standup import standup_send, standup_active, standup_start

from testing_fixtures.standup_test_fixtures import setup_test_interface

# ----- Success Send
# Extremely limited ways to test this without accessing the data structure.
def test_standup_active_success(setup_test_interface):
    user1, _, channel_id = setup_test_interface
    standup_start(user1["token"], channel_id, 100)

    assert (standup_send(user1["token"], channel_id, "General Kenobi")) == {}

# ----- Fail Send
def test_invalid_token(setup_test_interface):
    _, _, channel_id = setup_test_interface

    with pytest.raises(AccessError):
        standup_active(-999, channel_id, 'General Kenobi')
    with pytest.raises(AccessError):
        standup_active('fake_token', channel_id, 'General Kenobi')

def test_invalid_channel_id(setup_test_interface):
    user1, _, channel_id = setup_test_interface
    standup_start(user1["token"], channel_id, 100)

    with pytest.raises(InputError):
        standup_send(user1["token"], -999, "General Kenobi")
    with pytest.raises(InputError):
        standup_send(user1["token"], 'fake_channel', "General Kenobi")

def test_invalid_message_string_size(setup_test_interface):
    user1, _, channel_id = setup_test_interface
    standup_start(user1["token"], channel_id, 100)

    letters = string.ascii_letters
    message_str = ''.join(random.choice(letters) for i in range(1005))

    with pytest.raises(InputError):
        standup_send(user1["token"], channel_id, message_str)

def test_no_standup(setup_test_interface):
    user1, _, channel_id = setup_test_interface

    with pytest.raises(InputError):
        standup_send(user1["token"], channel_id, "General Kenobi")

def test_unauthorised_user(setup_test_interface):
    user1, user2, channel_id = setup_test_interface
    standup_start(user1["token"], channel_id, 'General Kenobi')

    with pytest.raises(AccessError):
        standup_send(user2["token"], channel_id, "General Kenobi")
'''
