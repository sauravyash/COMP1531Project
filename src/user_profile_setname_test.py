from channel import channel_invite
from channel import channel_messages
from error import InputError
from error import AccessError
import auth
import channels
import other
import pytest
import random
import string
from user import user_profile_setname

def create_user_1():
    
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

def valid_test():

    create_user_1()
    first_name = "fname"
    last_name = "lname"

    assert( user_profile_setname(result["token"], first_name, last_name) == {} )

def invalid_token_test():

    create_user_1()
    first_name = "fname"
    last_name = "lname"

    with pytest.raises(InputError):
        user_profile_setname("invalid_token", first_name, last_name) 

def test_invalid_first_name():

    create_user_1()
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(55))

    first_name = result_str
    last_name = "lname"

    with pytest.raises(InputError):
        user_profile_setname(result["token"], first_name, last_name)

def test_invalid_last_name():

    create_user_1()
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(55))

    first_name = "fname"
    last_name = result_str

    with pytest.raises(InputError):
        user_profile_setname(result["token"], first_name, last_name)

def test_invalid_full_name():

    create_user_1()
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(55))
    first_name = result_str
    last_name = result_str

    with pytest.raises(InputError):
        user_profile_setname(result["token"], first_name, last_name)

def test_empty_name():

    create_user_1()
    first_name = ""
    last_name = ""

    with pytest.raises(InputError):
        user_profile_setname(result["token"], first_name, last_name)








