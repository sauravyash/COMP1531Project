'''
import functions
'''
import pytest
import auth
import channels
import other
from channel import channel_invite
from error import InputError
from error import AccessError
# assume message id is an int
from message import message_send
from message import message_remove

def create_test_channel():
    '''
    create test channel for messages
    '''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("newvalidemail@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("newvalidemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel_invite(result["token"], channel_id["channel_id"], result1["u_id"])

    return (result, result1, channel_id)

# Success Messages Remove
# Remove must be from owner of the channel or sender of the message
# Owner/Sender token must be valid
# Channel id must be valid
def test_valid_message_remove():
    '''
    Success Messages Remove
    Remove must be from owner of the channel or sender of the message
    Owner/Sender token must be valid
    Channel id must be valid
    '''
    other.clear()
    result, result1, channel_id = create_test_channel()
    message_send(result["token"], channel_id["channel_id"], "Hello")
    m_id = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    assert message_remove(result1["token"], m_id["message_id"]) == {}

def test_valid_message_remove_channel_owner():
    '''
    message remove from the channel owner
    '''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("newvalidemail@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("newvalidemail@gmail.com", "password123")

    auth.auth_register("goodemail@gmail.com", "password123", "fname2", "lname2")
    result2 = auth.auth_login("goodemail@gmail.com", "password123")

    channel_id = channels.channels_create(result1["token"], "channel_1", True)
    channel_invite(result1["token"], channel_id["channel_id"], result2["u_id"])

    m_id = message_send(result2["token"], channel_id["channel_id"], "Funky Monkey")
    assert message_remove(result1["token"], m_id["message_id"]) == {}

def test_valid_message_remove_flockr_owner():
    '''
    the message is removed
    '''

    result, result1, channel_id = create_test_channel()
    message_send(result["token"], channel_id["channel_id"], "Hello")
    m_id = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    assert message_remove(result["token"], m_id["message_id"]) == {}

# Fail
def test_invalid_message_token():
    '''
    When the token is Invalid
    '''

    result, result1, channel_id = create_test_channel()
    message_send(result["token"], channel_id["channel_id"], "Hello")
    m_id = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    with pytest.raises(AccessError):
        message_remove("Invalid token", m_id["message_id"])


def test_invalid_message_id():
    '''
    When the message id is invalid
    '''

    result, result1, channel_id = create_test_channel()
    message_send(result["token"], channel_id["channel_id"], "Hello")
    message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    with pytest.raises(InputError):
        message_remove(result1["token"], 123)

def test_invalid_message_removed():
    '''
    When the message is already removed
    '''

    result, result1, channel_id = create_test_channel()
    message_send(result["token"], channel_id["channel_id"], "Hello")
    m_id = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    message_remove(result1["token"], m_id["message_id"])

    with pytest.raises(InputError):
        message_remove(result1["token"], m_id["message_id"])


def test_invalid_message_remove_not_sender():
    '''
    When the remove is not from the sender
    '''
    result, result1, channel_id = create_test_channel()

    auth.auth_register("awsome_email2@gmail.com", "password123", "fname2", "lname2")
    result2 = auth.auth_login("awsome_email2@gmail.com", "password123")
    channel_invite(result1["token"], channel_id["channel_id"], result2["u_id"])

    message_send(result["token"], channel_id["channel_id"], "Edit next message")
    m_id = message_send(result["token"], channel_id["channel_id"], "Funky Monkey")

    with pytest.raises(AccessError):
        message_remove(result2["token"], m_id["message_id"])


def test_invalid_message_remove_not_authorized():
    '''
    When the remove is not from owner of the channel
    '''

    result, result1, channel_id = create_test_channel()
    m_id = message_send(result["token"], channel_id["channel_id"], "Funky Monkey")
    with pytest.raises(AccessError):
        message_remove(result1["token"], m_id["message_id"])
