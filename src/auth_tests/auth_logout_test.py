''' Auth logout tests
This file contains all test cases for auth logout function.

'''
import auth
import other
import pytest
from error import AccessError
from testing_fixtures.auth_test_fixtures import setup_test_interface

# ----- Successful logouts
def test_logout(setup_test_interface):
    '''
    Success logout
    Valid token
    '''
    user = setup_test_interface

    tok = user["token"]

    assert(auth.auth_logout(tok)["is_success"] == True)

# ----- Unsuccesful logouts
def test_already_logged_out(setup_test_interface):
    '''
    Unsuccesful logout
    Invalid token (user already logged out)
    '''
    user = setup_test_interface

    tok = user["token"]

    # Logout a user.
    auth.auth_logout(tok)
    # Check that if user is already logged out, logout fails.
    assert(auth.auth_logout(tok)["is_success"] == False)

def test_invalid_token(setup_test_interface):
    '''
    Unsuccesful logout
    Invalid token (token not found)
    '''
    user = setup_test_interface

    tok = user["token"]

    # Check that an access error is raised if token is invalid.
    with pytest.raises(AccessError):
        auth.auth_logout("Invalid token")
