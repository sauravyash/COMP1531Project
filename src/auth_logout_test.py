''' Auth logout tests
This file contains all test cases for auth logout function.

'''
import auth
import other
import pytest
from error import AccessError

# ----- Successful logouts
def test_logout():
    other.clear()
    # Register and login a user.
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    auth.auth_login('validemail@gmail.com', 'validpassword')
    # Successfully log them out.
    assert(auth.auth_logout(result["token"])["is_success"] == True)

# ----- Unsuccesful logouts
def test_already_logged_out():
    other.clear()
    # Register and login a user.
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    auth.auth_login('validemail@gmail.com', 'validpassword')
    # Logout a user.
    auth.auth_logout(result["token"])
    # Check that if user is already logged out, logout fails.
    assert(auth.auth_logout(result["token"])["is_success"] == False)

def test_invalid_token():
    other.clear()
    # Register and login a user.
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    auth.auth_login('validemail@gmail.com', 'validpassword')
    # Check that an access error is raised if token is invalid.
    with pytest.raises(AccessError):
        auth.auth_logout("Invalid token")
