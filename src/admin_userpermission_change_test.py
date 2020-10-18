from channel import channel_invite
from channel import channel_messages
from error import InputError
from error import AccessError
import auth
import channels
import other
import pytest
import random
import string
from user import admin_userpermission_change

def create_users_and_channels():

    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("cool_email@gmail.com", "password123", "fname1", "lname1")
    result_1 = auth.auth_login("cool_email@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    channel_invite(result["token"], channel_id["channel_id"], result_1["u_id"])


def test_valid_test():

    create_users_and_channels()
    assert( admin_userpermission_change(result['token'],result_1['u_id'],1) == {} )

def test_invalid_test_uId():

    create_users_and_channels()

    with pytest.raises():
        admin_userpermission_change(result['token'],-1,1)

def test_invalid_permission_Id():

    create_users_and_channels()
    with pytest.raises():
        admin_userpermission_change(result['token'],result_1['u_id'],99)

def test_user_not_owner_1():

    create_users_and_channels()

    auth.auth_register("awesome_email@gmail.com", "password123", "fname2", "lname2")
    result_2 = auth.auth_login("awesome_email@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    channel_invite(result["token"], channel_id["channel_id"], result_2["u_id"])
    
    with pytest.raises(AccessError):
        admin_userpermission_change(result_1["token"],result_2["u_id"],1)

def test_user_not_owner_2():

    create_users_and_channels()
    
    with pytest.raises(AccessError):
        admin_userpermission_change(result_1["token"],result["u_id"],2)










