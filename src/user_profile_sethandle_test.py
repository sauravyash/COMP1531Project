'''tests for user_profile_sethandle'''
import pytest
from error import InputError
import auth
import other
from user import user_profile_sethandle

def test_valid_handle():
    '''test for valid handle'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    user_profile_sethandle(result["token"], "newhandle")

def test_invalid_handle_short():
    '''test for invalid short handle'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    with pytest.raises(InputError):
        user_profile_sethandle(result["token"], "ah")

def test_invalid_handle_long():
    '''test for invalid long handle'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    with pytest.raises(InputError):
        user_profile_sethandle(result["token"], "handlehasmorethantwentycharacters")

def test_handle_already_used():
    '''tests for handle which is already used'''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("validemail2@gmail.com", "password", "Andy", "Huang")
    auth.auth_login("validemail2@gmail.com", "password")

    with pytest.raises(InputError):
        user_profile_sethandle(result["token"], "andyhuang")
