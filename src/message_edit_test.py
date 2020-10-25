'''
import functions
'''
import random
import string
import pytest
import other
import auth
import channels
import channel
from error import InputError, AccessError
# assume message id is an int
from message import message_send, message_edit


def create_test_channel():
    '''
    creates the channel for testing
    '''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("goodemail@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("goodemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel.channel_invite(result["token"], channel_id["channel_id"], result1["u_id"])

    return (result, result1, channel_id)

def test_valid_message_edit():
    '''
    Success Messages
    Valid sender token
    Valid message ID
    Edited message within 1000 charactre limit
    Edit authorized by owner or sender
    '''
    _, result1, channel_id = create_test_channel()
    #message_send(result["token"], channel_id["channel_id"], "Hello")
    m_id = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    assert message_edit(result1["token"], m_id["message_id"], "Monkey Funky") == {}
    msgs = channel.channel_messages(result1["token"], channel_id["channel_id"], 0)

    assert msgs["messages"][0]['message'] == "Monkey Funky"

def test_authorized_edit_owner():
    '''
    Success Messages
    Valid sender token
    Valid message ID
    Edited message within 1000 charactre limit
    Edit authorized by owner or sender
    '''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("goodemail@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("goodemail@gmail.com", "password123")

    auth.auth_register("coolemail@gmail.com", "password123", "fname2", "lname2")
    result2 = auth.auth_login("coolemail@gmail.com", "password123")

    channel_id = channels.channels_create(result1["token"], "channel_1", True)
    channel.channel_invite(result1["token"], channel_id["channel_id"], result2["u_id"])
    channel.channel_invite(result1["token"], channel_id["channel_id"], result["u_id"])
    m_id = message_send(result2["token"], channel_id["channel_id"], "Funky Monkey")
    assert message_edit(result1["token"], m_id["message_id"], "Monkey Funky") == {}

def test_authorized_edit_flockr_owner():
    '''
    Authorized from the owner of the flockr
    '''
    result, result1, channel_id = create_test_channel()
    m_id = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    assert message_edit(result["token"], m_id["message_id"], "Monkey Funky") == {}


#Fail
def test_invalid_token():
    '''
    Invalid sender/owner token
    '''
    result, result1, channel_id = create_test_channel()
    message_send(result["token"], channel_id["channel_id"], "Hello")
    m_id = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    with pytest.raises(AccessError):
        message_edit("Invalid token", m_id["message_id"], "Monkey Funky")

def test_invalid_message_id():
    '''
    Invalid message ID
    '''
    result, result1, channel_id = create_test_channel()
    message_send(result["token"], channel_id["channel_id"], "Hello")
    message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    with pytest.raises(InputError):
        message_edit(result1["token"], -1, "Monkey Funky")

def test_invalid_message_edit_exceeds_size_limit():
    '''
    Message edit size exceeds 1000'
    '''
    result, result1, channel_id = create_test_channel()
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(1005))
    m_id = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    with pytest.raises(InputError):
        message_edit(result["token"], m_id["message_id"], result_str)

def test_invalid_message_edit_not_sender():
    '''
    Edit not from the sender
    '''

    result, result1, channel_id = create_test_channel()
    auth.auth_register("awsome_email@gmail.com", "password123", "fname2", "lname2")
    result2 = auth.auth_login("awsome_email@gmail.com", "password123")
    channel.channel_invite(result["token"], channel_id["channel_id"], result2["u_id"])

    m_id = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    with pytest.raises(AccessError):
        message_edit(result2["token"], m_id["message_id"], "Monkey Funky")


def test_invalid_message_edit_not_authorized():
    '''
    Member trying to edit owner message
    '''
    result, result1, channel_id = create_test_channel()
    m_id = message_send(result["token"], channel_id["channel_id"], "Funky Monkey")
    with pytest.raises(AccessError):
        message_edit(result1["token"], m_id["message_id"], "Monkey Funky")
