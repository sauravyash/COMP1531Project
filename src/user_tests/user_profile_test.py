'''
import functions
'''
import pytest
import auth
import other
from user import user_profile
from error import InputError
from error import AccessError
from testing_fixtures.user_test_fixtures import setup_test_interface

def test_invalid_user_profile(setup_test_interface):
    '''
    Unsuccessful user profile
    Invalid user id
    '''
    user = setup_test_interface

    tok = user["token"]

    with pytest.raises(InputError):
        user_profile(tok, 0)


def test_invalid_user_profile_token(setup_test_interface):
    '''
    Unsuccessful name change
    Invalid first name (empty)
    Valid last name
    '''
    user = setup_test_interface

    u_id = user["u_id"]

    with pytest.raises(AccessError):
        user_profile("INVALID TOKEN", u_id)
