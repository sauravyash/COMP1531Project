'''tests for user_profile_sethandle'''
import pytest
from error import InputError
import auth
import other
from user import user_profile_sethandle
from testing_fixtures.user_test_fixtures import setup_test_interface

def test_valid_handle(setup_test_interface):
    '''
    Success handle change
    Valid token
    Valid handle
    '''
    user = setup_test_interface

    tok = user["token"]

    user_profile_sethandle(tok, "newhandle")

def test_invalid_handle_short(setup_test_interface):
    '''
    Unsuccessful handle change
    Invalid handle (too short)
    '''
    user = setup_test_interface

    tok = user["token"]

    with pytest.raises(InputError):
        user_profile_sethandle(tok, "ah")

def test_invalid_handle_long(setup_test_interface):
    '''
    Unsuccessful handle change
    Invalid handle (too long)
    '''
    user = setup_test_interface

    tok = user["token"]

    with pytest.raises(InputError):
        user_profile_sethandle(tok, "handlehasmorethantwentycharacters")

def test_handle_already_used(setup_test_interface):
    '''
    Unsuccessful handle change
    Invalid handle (already in use)
    '''
    user = setup_test_interface

    tok = user["token"]

    auth.auth_register("validemail2@gmail.com", "password", "Some", "One")
    auth.auth_login("validemail2@gmail.com", "password")

    with pytest.raises(InputError):
        user_profile_sethandle(tok, "someone")
