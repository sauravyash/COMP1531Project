###########################################Channel Deatil Tests################################
from channel import channel_details
from channel import channel_invite
from error import AccessError
from error import InputError
import auth
import channels
import other
import pytest
# Success Showing Detail
def test_valid_details_public():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])

    assert channel_details(result1["token"], channel_id["channel_id"])

def test_valid_details_private():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", False)

    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])

    assert channel_details(result1["token"], channel_id["channel_id"])

# Fail Showing Detail
def test_invalid_details_not_member():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    auth.auth_register("validemail2@gmail.com", "password123", "fname2", "lname2")
    result2 = auth.auth_login("validemail2@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])

    with pytest.raises(AccessError):
        channel_details(result2["token"], channel_id["channel_id"])

def test_invalid_details_channel_id_public():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])

    with pytest.raises(InputError):
        channel_details(result1["token"], -1)

def test_invalid_details_channel_id_private():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", False)

    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])

    with pytest.raises(InputError):
        channel_details(result1["token"], -1)
