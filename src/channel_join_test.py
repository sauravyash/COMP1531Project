############################################Channel Join Tests###################################
from channel import channel_invite
from channel import channel_join
from error import InputError
from error import AccessError
import auth
import channels
import other
import pytest
# Success Join
def test_valid_join_public_owner():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    assert channel_join(result["token"], channel_id["channel_id"]) == {}

def test_valid_join_public_memeber():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    assert channel_join(result1["token"], channel_id["channel_id"]) == {}


def test_valid_join_private_owner():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", False)
    assert channel_join(result["token"], channel_id["channel_id"]) == {}


# Fail Join
def test_invalid_public_channel_id():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])
    with pytest.raises(InputError):
        channel_join(result1["token"], -1)

def test_invalid_private_channel_id():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", False)
    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])
    with pytest.raises(InputError):
        channel_join(result1["token"], -1)

def test_invalid_join_not_authorized():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", False)
    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])   
    with pytest.raises(AccessError):
        channel_join(result1["token"], channel_id["channel_id"])
