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
from user import user_profile_sethandle

def test_valid_handle():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    user_profile_sethandle(result["token"], "newhandle")

def test_invalid_handle_short():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    with pytest.raises(InputError):
        user_profile_sethandle(result["token"], "ah")

def test_invalid_handle_long():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    with pytest.raises(InputError):
        user_profile_sethandle(result["token"], "handlehasmorethantwentycharacters")

def test_handle_already_used():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail2@gmail.com", "password", "Andy", "Huang")
    result1 = auth.auth_login("validemail2@gmail.com", "password")

    with pytest.raises(InputError):
        user_profile_sethandle(result["token"], "andyhuang")
