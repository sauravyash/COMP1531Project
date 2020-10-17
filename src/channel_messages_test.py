#######################################Channel Messages Test#############################
from channel import channel_invite
from channel import channel_messages
from error import InputError
from error import AccessError
import auth
import channels
import other
import pytest

# Success Messages
def test_valid_channel_message():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])

    assert channel_messages(result1["token"], channel_id["channel_id"], 0) == {
        'messages': [],
        'start': 0,
        'end': -1,
    }

# Fail
def test_invalid_channel_messages_ID():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])

    with pytest.raises(InputError):
        channel_messages(result1["token"], -1, 0)

def test_invalid_channel_messages_start():
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
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", False)

    with pytest.raises(AccessError):
        channel_messages(result1["token"], channel_id["channel_id"], 0)
