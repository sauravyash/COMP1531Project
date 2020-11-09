'''These are the tests for user_profile_setname '''

import pytest
from error import InputError
import auth
import other
from user import user_profile_setname
from testing_fixtures.user_test_fixtures import setup_test_interface

def test_valid_name(setup_test_interface):
    '''
    Success name change
    Valid token
    Valid first name
    Valid last name
    '''
    user = setup_test_interface

    tok = user["token"]

    user_profile_setname(tok, "newfname", "newlname")

def test_invalid_fname(setup_test_interface):
    '''
    Unsuccessful name change
    Invalid first name (empty)
    Valid last name
    '''
    user = setup_test_interface

    tok = user["token"]

    with pytest.raises(InputError):
        user_profile_setname(tok, "", "newlname")

def test_invalid_lname(setup_test_interface):
    '''
    Unsuccessful name change
    Valid first name
    Invalid last name (empty)
    '''
    user = setup_test_interface

    tok = user["token"]

    with pytest.raises(InputError):
        user_profile_setname(tok, "newfname", "")

def test_invalid_longfname(setup_test_interface):
    '''
    Unsuccessful name change
    Invalid first name (too long)
    Valid last name
    '''
    user = setup_test_interface

    tok = user["token"]

    long_name = "newfirstnamewhichiscertainlymorethanfiftycharacterslong"
    with pytest.raises(InputError):
        user_profile_setname(tok, long_name, "newlname")

def test_invalid_longlname(setup_test_interface):
    '''
    Unsuccessful name change
    Valid first name
    Invalid last name (too long)
    '''
    user = setup_test_interface

    tok = user["token"]

    long_name = "newfirstnamewhichiscertainlymorethanfiftycharacterslong"
    with pytest.raises(InputError):
        user_profile_setname(tok, "newfname", long_name)
