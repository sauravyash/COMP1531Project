import auth
import channels
import other
import pytest
import random
import string
from channel import channel_invite
from channel import channel_messages
from error import InputError
from error import AccessError

from user import user_profile

# Success user_profile
#def test_valid_user_profile(): can't be blackbox?
#    other.clear()
#    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
#    result = auth.auth_login("validemail@gmail.com", "password123")



def test_invalid_user_profile():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    with pytest.raises(InputError):
        user_profile(result["token"], 0)


#def create_test_user():
#    other.clear()
#    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
#    result = auth.auth_login("validemail@gmail.com", "password123")
#
#    auth.auth_register("good_email@gmail.com", "password123", "fname1", "#lname1")
#    result1 = auth.auth_login("good_email@gmail.com", "password123")

# Success User_profile
# Valid token and valid user ID
# returns user_id, email, first name, last name, and handle
#def test_valid_user_profile():
#
#    #create_test_user()
###
    #auth.auth_register("good_email@gmail.com", "password123", "fname1", "lname1")
#    result1 = auth.auth_login("good_email@gmail.com", "password123")
#    # crossponding dictionary with same id and token
#    assert user_profile(result1["token"], result1["u_id"]) == users["users"]


# Fail
# invalid/not registered token
#def test_invalid_user_profile():

    #create_test_user()
#    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
#    result = auth.auth_login("validemail@gmail.com", "password123")
##    auth.auth_register("good_email@gmail.com", "password123", "fname1", "l#name1")
#    result1 = auth.auth_login("good_email@gmail.com", "password123")
    # crossponding dictionary with same id and token
#    with pytest.raises(InputError):
#        #user_profile(result2["token"], result2["u_id"])
#        user_profile(result1["token"], 0)

# Empty Input
#def test_invalid_user_profile_empty():
#
    #create_test_user()
#    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
#    result = auth.auth_login("validemail@gmail.com", "password123")
#
#    auth.auth_register("good_email@gmail.com", "password123", "fname1", "#lname1")
#    result1 = auth.auth_login("good_email@gmail.com", "password123")
#    # crossponding dictionary with same id and token
#    with pytest.raises(InputError):
#        user_profile("", result2["u_id"])
