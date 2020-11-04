'''Import functions'''
import pytest
import auth
import channel
import channels
import other
from error import InputError
from error import AccessError
from message import message_send, message_react

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


def test_success_react():
    ''' Success message react case'''

    _, result1, channel_id = create_test_channel()

    m_id = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")

    assert (message_react(result1["token"], m_id["message_id"], 1)) == {}


def test_invalid_message_id():
    '''Invalid message ID'''
    _, result1, channel_id = create_test_channel()

    message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")

    with pytest.raises(InputError):
        message_react(result1["token"], -1, 1)



def test_invalid_react_id():
    '''Invalid message react ID'''
    _, result1, channel_id = create_test_channel()

    m_id = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")

    with pytest.raises(InputError):
        message_react(result1["token"], m_id["message_id"], -999)



def test_react_already_exist():
    '''Invalid message react ID'''
    _, result1, channel_id = create_test_channel()

    m_id = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")

    message_react(result1["token"], m_id["message_id"], 1)

    with pytest.raises(InputError):
        message_react(result1["token"], m_id["message_id"], 1)
