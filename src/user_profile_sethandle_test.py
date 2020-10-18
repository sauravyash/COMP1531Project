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
from user import user_profile_sethandle

def create_user_1():

    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")


def test_valid():

    create_user_1()
    assert ( user_profile_sethandle(result['token'],"Nabriu") == {} )


def test_invalid_less_than_3():

    create_user_1()
    with pytest.raises(InputError):
        user_profile_sethandle(result['token'], "Na")


def test_invalid_more_than_20():

    create_user_1()
    with pytest.raises(InputError):
        user_profile_sethandle(result['token'], "Nabriu_AMHunter_Winny")


def test_invalid_sethandle_used():

    create_user_1()
    auth.auth_register("cool_email@gmail.com", "password123", "funkey", "monkey")
    result_1 = auth.auth_login("cool_email@gmail.com", "password123")

    user_profile_sethandle(result['token'], "Nabriu_AMHunter")

    with pytest.raises(InputError):
        user_profile_sethandle(result_1['token'], "Nabriu_AMHunter")

def test_invalid_empty_string():

    create_user_1()
    with pytest.raises(InputError):
        user_profile_sethandle(result_1['token'], "")

def test_invalid_white_spaces():

    create_user_1()
    with pytest.raises(InputError):
        user_profile_sethandle(result_1['token'], "    ")














