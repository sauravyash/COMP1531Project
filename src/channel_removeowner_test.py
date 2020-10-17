#############################################Channel Removeowner Tests############################
from channel import channel_invite
from channel import channel_removeowner
from error import AccessError
from error import InputError
import auth
import channels
import other
import pytest
# Success removeowner
def test_valid_removeowner():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    # owner remove owner
    assert channel_removeowner(result["token"], channel_id["channel_id"], result["u_id"]) == {}

# Fail removeowner
def test_invalid_removeowner_channel_ID():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])

    with pytest.raises(InputError):
        channel_removeowner(result["token"], -1, result["u_id"])

def test_invalid_removeowner_not_owner():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])

    with pytest.raises(InputError):
        channel_removeowner(result["token"], channel_id["channel_id"], result1["u_id"])

def test_invalid_removeowner_not_authorised():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])

    with pytest.raises(AccessError):
        channel_removeowner(result1["token"], channel_id["channel_id"], result["u_id"])
