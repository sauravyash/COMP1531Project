''' Testing function: users/all (users_all)
'''

import pytest

import auth
import channels
import other
import random
import string

from channel import channel_invite
from channel import channel_messages

from error import InputError
from error import AccessError

from other import users_all

# Success users_all
# Valid user token
# Returns a list of all users and their associated details

def test_users_all():
    other.clear()
    
    users = [
        {
            'fname': 'fname',
            'lname': 'lname',
            'email': 'validemail@gmail.com'
        },
        {
            'fname': 'fname1',
            'lname': 'lname1',
            'email': 'validemail1@gmail.com'
        },
        {
            'fname': 'fname2',
            'lname': 'lname2',
            'email': 'validemail2@gmail.com'
        },
        {
            'fname': 'fname3',
            'lname': 'lname3',
            'email': 'validemail3@gmail.com'
        },
        {
            'fname': 'fname4',
            'lname': 'lname4',
            'email': 'validemail4@gmail.com'
        }
    ]
    
    result = []

    for user in users:
        auth.auth_register(user["email"], "GenericPwd1", user["fname"], user["lname"])
        result.append(auth.auth_login(user["email"], "GenericPwd1"))
    
    fetched_users = users_all(result[0]['token'])['users']

    for i, user in enumerate(fetched_users):
        assert user['email'] == users[i]['email']
        assert user["name_last"] == users[i]['lname']
        assert user['name_first'] == users[i]['fname']

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

    assert users_all(result["token"]) == users
