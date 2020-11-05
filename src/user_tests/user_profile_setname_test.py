'''These are the tests for user_profile_setname '''

import pytest
from error import InputError
import auth
import other
from user import user_profile_setname

def test_valid_name():
    '''tests valid name'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    user_profile_setname(result["token"], "newfname", "newlname")

def test_invalid_fname():
    '''tests invalid first name'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    with pytest.raises(InputError):
        user_profile_setname(result["token"], "", "newlname")

def test_invalid_lname():
    '''tests invalid last name'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    with pytest.raises(InputError):
        user_profile_setname(result["token"], "newfname", "")

def test_invalid_longfname():
    '''tests invalid long first name'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    long_name = "newfirstnamewhichiscertainlymorethanfiftycharacterslong"
    with pytest.raises(InputError):
        user_profile_setname(result["token"], long_name, "newlname")

def test_invalid_longlname():
    '''tests invalid long last name'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")
    long_name = "newfirstnamewhichiscertainlymorethanfiftycharacterslong"
    with pytest.raises(InputError):
        user_profile_setname(result["token"], "newfname", long_name)
