'''Channel message test'''
import pytest
import auth
import channels
import other

from channel import channel_invite
from channel import channel_messages
from error import InputError
from error import AccessError
from message import message_send


# Success Messages
def test_valid_channel_message():
    '''Success Messages'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])
    message_send(result1["token"], channel_id["channel_id"], "Hello There")
    check = channel_messages(result1["token"], channel_id["channel_id"], 0)
    assert check["end"] == -1
    assert check["start"] == 0
    assert check["messages"][0]["u_id"] == 2
    assert check["messages"][0]["message"] == "Hello There"

# Fail
def test_invalid_channel_messages_id():
    ''' Invalid Channel ID'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])

    with pytest.raises(InputError):
        channel_messages(result1["token"], 15, 0)

def test_invalid_channel_messages_start():
    ''' Invalid Start'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])

    with pytest.raises(InputError):
        channel_messages(result1["token"], channel_id["channel_id"], -1)

def test_invalid_channel_messages_authorised():
    ''' not a member of the channel'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", False)

    with pytest.raises(AccessError):
        channel_messages(result1["token"], channel_id["channel_id"], 0)
