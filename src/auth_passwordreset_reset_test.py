''' Import Functions '''
import random
import string
import pytest
import other
import auth
import channels
import channel
from error import InputError, AccessError
from auth import auth_passwordreset_request, auth_passwordreset_reset

#def test_auth_passwordreset_reset_success():
#    ''' Success auth passwordreset case'''
#    other.clear()

#    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
#    auth_passwordreset_request("coolemail@gmail.com")

#    assert auth_passwordreset_reset("reset_code","abc123") == {}

def test_invalid_reset_code():
    ''' tests for an invalid reset code'''
    other.clear()

    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    auth_passwordreset_request("coolemail@gmail.com")

    with pytest.raises(InputError):
        auth_passwordreset_reset("invalid_reset_code","abc123")

#def test_invalid_password():
#    ''' tests for an invalid password'''
#    other.clear()

#    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
#    auth_passwordreset_request("coolemail@gmail.com")

#    with pytest.raises(InputError):
        # Passwords which are less than 6 characters long are invalid
#        auth_passwordreset_reset("reset_code","pass")
