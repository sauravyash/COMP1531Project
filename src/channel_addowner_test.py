#############################################Channel Addowner Tests###############################
from channel import channel_addowner
from channel import channel_invite
from error import AccessError
from error import InputError
import auth
import channels
import other
import pytest
# Success adding owner
def test_valid_addowner_public():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")
    channel_id = channels.channels_create(result["token"], "channel_1", True)

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])

    assert channel_addowner(result["token"], channel_id["channel_id"], result1["u_id"]) == {}


# Fail adding owner
def test_invalid_addowner_channel_ID():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])

    with pytest.raises(InputError) as e:
        channel_addowner(result["token"], -1, result1["u_id"])

def test_invalid_addowner_user_ID():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])

    with pytest.raises(InputError) as e:
        channel_addowner(result1["token"], channel_id["channel_id"], -1)

def test_invalid_addowner_is_already_owner():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    # owner trying to add itself as owner
    with pytest.raises(AccessError) as e:
        channel_addowner(result["token"], channel_id['channel_id'], result["u_id"])

def test_invalid_addowner_not_authorized():
    other.clear()
    # owner
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    # member
    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])

    # member trying to addowner
    with pytest.raises(AccessError) as e:
        channel_addowner(result1["token"], channel_id['channel_id'], result["u_id"])