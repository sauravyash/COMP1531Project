''' Import Functions '''
import random
import string
import pytest
import other
import auth
import channels
import channel
from error import InputError, AccessError
from auth import auth_passwordreset_request

def test_auth_passwordreset_request_success():
    ''' Success auth passwordreset request case'''
    other.clear()

    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    auth_passwordreset_request("coolemail@gmail.com")

    assert auth_passwordreset_request("coolemail@gmail.com") == {}
