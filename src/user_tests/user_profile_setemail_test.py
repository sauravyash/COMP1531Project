'''tests for user_profile_setemail'''
import pytest
from error import InputError
import auth
import other
from user import user_profile_setemail
from testing_fixtures.user_test_fixtures import setup_test_interface

def test_valid_email(setup_test_interface):
    '''
    Success email change
    Valid token
    Valid email
    '''
    user = setup_test_interface

    tok = user["token"]

    user_profile_setemail(tok, "newvalidemail@gmail.com")

def test_invalid_email(setup_test_interface):
    ''''
    Unsuccessful email change
    Invalid email
    '''
    user = setup_test_interface

    tok = user["token"]

    with pytest.raises(InputError):
        user_profile_setemail(tok, "invalidemail.com")

def test_email_used(setup_test_interface):
    '''
    Unsuccessful email change
    Invalid email (email already in use)
    '''
    user = setup_test_interface

    tok = user["token"]

    auth.auth_register("alsovalidemail@gmail.com", "password123", "fname1", "lname1")
    auth.auth_login("alsovalidemail@gmail.com", "password123")

    with pytest.raises(InputError):
        user_profile_setemail(tok, "alsovalidemail@gmail.com")
