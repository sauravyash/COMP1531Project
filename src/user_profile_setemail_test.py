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
from user import user_profile_setemail

def create_user_1():

    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

def test_valid_1():

    create_user_1()
    assert ( user_profile_setemail(result['token'],"address@gmail.com") == {} )

def test_valid_2():

    create_user_1()
    assert ( user_profile_setemail(result['token'],"cool.email@gmail.com") == {} )


def test_email_used():

    create_user_1()

    auth.auth_register("cool_email@yahoo.com", "password123", "fname1", "lname1")
    result_1 = auth.auth_login("cool_email@yahoo.com", "password123")

    with pytest.raises(InputError):
        user_profile_setemail( result['token'] , "cool_email@yahoo.com")


def test_invalid_email_1():

    create_user_1()
    with pytest.raises(InputError):
        user_profile_setemail( result['token'] , "iluvfortnite.com" )

def test_invalid_email_2():
    
    create_user_1()
    with pytest.raises(InputError):
        user_profile_setemail( result['token'] , "hello123@gmail ")


def test_empty_email():

    create_user_1()
    with pytest.raises(InputError):
        user_profile_setemail( result['token'] , "")


def test_empty_spaces_email():

    create_user_1()
    with pytest.raises(InputError):
        user_profile_setemail( result['token'] , "    ")
    






        







