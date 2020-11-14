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


def test_invalid_reset_code():
    ''' tests for an invalid reset code'''
    other.clear()

    auth.auth_register("comp1531wed13grape3noreply@gmail.com", "password123", "fname", "lname")
    auth_passwordreset_request("comp1531wed13grape3noreply@gmail.com")

    with pytest.raises(InputError):
        auth_passwordreset_reset("invalid_reset_code","abc123")
