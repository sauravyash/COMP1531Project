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
from user import user_profile_setemail

def test_valid_email():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    user_profile_setemail(result["token"], "newvalidemail@gmail.com")

def test_invalid_email():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    with pytest.raises(InputError):
        user_profile_setemail(result["token"], "invalidemail.com")

def test_email_used():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("alsovalidemail@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("alsovalidemail@gmail.com", "password123")

    with pytest.raises(InputError):
        user_profile_setemail(result["token"], "alsovalidemail@gmail.com")
