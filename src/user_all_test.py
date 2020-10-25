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
            'email': 'validemail@gmail.com',
            'id': 1,
            'handle': "fnamelname"
        },
        {
            'fname': 'fname1',
            'lname': 'lname1',
            'email': 'validemail1@gmail.com',
            'id': 2,
            'handle': "fname1lname1"
        },
        {
            'fname': 'fname2',
            'lname': 'lname2',
            'email': 'validemail2@gmail.com',
            'id': 3,
            'handle': "fname2lname2"
        },
        {
            'fname': 'fname3',
            'lname': 'lname3',
            'email': 'validemail3@gmail.com',
            'id': 4,
            'handle': "fname3lname3"
        },
        {
            'fname': 'fname4',
            'lname': 'lname4',
            'email': 'validemail4@gmail.com',
            'id': 5,
            'handle': "fname4lname4"
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
        assert user['handle_str'] == users[i]['handle']
        assert user['user_id'] == users[i]['id']

#    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
#    result = auth.auth_login("validemail@gmail.com", "password123")

#    auth.auth_register("validemail1@gmail.com", "password123", "fname1", "lname1")
#    result1 = auth.auth_login("validemail1@gmail.com", "password123")

#    auth.auth_register("validemail2@gmail.com", "password123", "fname2", "lname2")
#    result2 = auth.auth_login("validemail2@gmail.com", "password123")

#    auth.auth_register("validemail3@gmail.com", "password123", "fname3", "lname3")
#    result3 = auth.auth_login("validemail3@gmail.com", "password123")

#    auth.auth_register("validemail4@gmail.com", "password123", "fname4", "lname4")
#    result4 = auth.auth_login("validemail4@gmail.com", "password123")

    #assert users_all(result[0]["token"]) == users
