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
from user import user_profile_setname

def test_valid_name():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    user_profile_setname(result["token"], "newfname", "newlname")

def test_invalid_fname():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    with pytest.raises(InputError):
        user_profile_setname(result["token"], "", "newlname")

def test_invalid_lname():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    with pytest.raises(InputError):
        user_profile_setname(result["token"], "newfname", "")

def test_invalid_longfname():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    with pytest.raises(InputError):
        user_profile_setname(result["token"], "newfirstnamewhichiscertainlymorethanfiftycharacterslong", "newlname")

def test_invalid_longlname():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    with pytest.raises(InputError):
        user_profile_setname(result["token"], "newfname", "newlastnamewhichiscertainlymorethanfiftycharacterslong")
