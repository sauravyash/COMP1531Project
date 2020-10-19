'''tests for admin_userpermission_change'''
import pytest
from channel import channel_invite
from error import AccessError
import auth
import channels
import other
from other import admin_userpermission_change

def test_valid_test():
    '''valid test'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("cool_email@gmail.com", "password123", "fname1", "lname1")
    result_1 = auth.auth_login("cool_email@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    channel_invite(result["token"], channel_id["channel_id"], result_1["u_id"])
    assert admin_userpermission_change(result['token'],result_1['u_id'],1) == {}

def test_invalid_uid():
    '''invalid userID test'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("cool_email@gmail.com", "password123", "fname1", "lname1")
    result_1 = auth.auth_login("cool_email@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel_invite(result["token"], channel_id["channel_id"], result_1["u_id"])

    with pytest.raises():
        admin_userpermission_change(result['token'],-1,1)

def test_invalid_permissionid():
    '''invalid permissionID test'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("cool_email@gmail.com", "password123", "fname1", "lname1")
    result_1 = auth.auth_login("cool_email@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel_invite(result["token"], channel_id["channel_id"], result_1["u_id"])

    with pytest.raises():
        admin_userpermission_change(result['token'],result_1['u_id'],99)

def test_user_not_owner_1():
    '''first test- user is not owner'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("cool_email@gmail.com", "password123", "fname1", "lname1")
    result_1 = auth.auth_login("cool_email@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel_invite(result["token"], channel_id["channel_id"], result_1["u_id"])

    auth.auth_register("awesome_email@gmail.com", "password123", "fname2", "lname2")
    result_2 = auth.auth_login("awesome_email@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel_invite(result["token"], channel_id["channel_id"], result_2["u_id"])

    with pytest.raises(AccessError):
        admin_userpermission_change(result_1["token"],result_2["u_id"],1)

def test_user_not_owner_2():
    '''second test- user is not owner'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("cool_email@gmail.com", "password123", "fname1", "lname1")
    result_1 = auth.auth_login("cool_email@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel_invite(result["token"], channel_id["channel_id"], result_1["u_id"])

    with pytest.raises(AccessError):
        admin_userpermission_change(result_1["token"],result["u_id"],2)
