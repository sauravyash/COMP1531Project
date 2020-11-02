'''Import functions'''
import pytest
import auth
import channel
import channels
import other
from error import InputError
from error import AccessError
from message import message_pin, message_send

def create_test_channel():
    '''creates the channel for testing'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("goodemail@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("goodemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel.channel_invite(result["token"], channel_id["channel_id"], result1["u_id"])

    return (result, result1, channel_id)


def test_success_pin():
    ''' Success message react case'''

    result, result1, channel_id = create_test_channel()

    m_id = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")

    assert (message_pin(result["token"], m_id["message_id"])) == {}


def test_invalid_message_id():
    '''Invalid message ID'''
    _, result1, channel_id = create_test_channel()

    message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")

    with pytest.raises(InputError):
        message_pin(result1["token"], -999)


def test_pin_already():
    '''Invalid message react ID'''
    _, result1, channel_id = create_test_channel()

    m_id = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")

    message_pin(result1["token"], m_id["message_id"])

    with pytest.raises(InputError):
        message_pin(result1["token"], m_id["message_id"])


def test_not_in_channel():
    '''User not a member'''
    other.clear()

    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("good_email@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("good_email@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    m_id = message_send(result["token"], channel_id["channel_id"], "Funky Monkey")

    with pytest.raises(AccessError):
        message_pin(result1["token"], m_id["message_id"])

def test_not_owner():
    '''User not owner'''
    other.clear()

    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("good_email@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("good_email@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel.channel_invite(result["token"], channel_id["channel_id"], result1["u_id"])

    m_id = message_send(result["token"], channel_id["channel_id"], "Funky Monkey")

    with pytest.raises(AccessError):
        message_pin(result1["token"], m_id["message_id"])