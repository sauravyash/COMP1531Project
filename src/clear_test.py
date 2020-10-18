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


from clear import clear

# Success
# return the program to its orginal state
def test_user_all():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("good_email@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("good_email@gmail.com", "password123")

    auth.auth_register("good_email@gmail.com", "password123", "fname2", "lname2")
    result2 = auth.auth_login("awsome_email@gmail.com", "password123")


    auth.auth_register("good_email@gmail.com", "password123", "fname3", "lname3")
    result3 = auth.auth_login("super_awsome_email@gmail.com", "password123")

    auth.auth_register("good_email@gmail.com", "password123", "fname4", "lname4")
    result4 = auth.auth_login("awsome_awsome_email@gmail.com", "password123")


    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel_invite(result4["token"], channel_id["channel_id"], result4["u_id"])

    channel_id = channels.channels_create(result["token"], "channel_2", True)
    channel_invite(result3["token"], channel_id["channel_id"], result3["u_id"])


    assert clear() == {}