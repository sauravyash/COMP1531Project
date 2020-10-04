###########################################Channel Leave Tests##################################
from channel import channel_invite
from channel import channel_leave
from channel import channel_join
from error import InputError
from error import AccessError
import auth
import channels
import other
import pytest
# Success Leave
def test_valid_leave_public():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")
    
    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel_join(result1["token"], channel_id["channel_id"])
    assert channel_leave(result1["token"], channel_id["channel_id"]) == {}


# Fail to leave
def test_invalid_leave_channel_ID_public():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    with pytest.raises(InputError) as e:
        channel_leave(result1["token"], -1)

def test_invalid_leave_channel_ID_private():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", False)

    with pytest.raises(InputError) as e:
        channel_leave(result["token"], -1)

def test_invalid_leave_not_member():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", False)

    with pytest.raises(AccessError) as e:
        channel_leave(result1["token"], channel_id["channel_id"])