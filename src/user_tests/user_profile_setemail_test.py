'''tests for user_profile_setemail'''
import pytest
from error import InputError
import auth
import other
from user import user_profile_setemail

def test_valid_email():
    '''tests valid email'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    user_profile_setemail(result["token"], "newvalidemail@gmail.com")

def test_invalid_email():
    '''tests invalid email'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    with pytest.raises(InputError):
        user_profile_setemail(result["token"], "invalidemail.com")

def test_email_used():
    '''tests email used'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("alsovalidemail@gmail.com", "password123", "fname1", "lname1")
    auth.auth_login("alsovalidemail@gmail.com", "password123")

    with pytest.raises(InputError):
        user_profile_setemail(result["token"], "alsovalidemail@gmail.com")
