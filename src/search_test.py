from channel import channel_invite
from channel import channel_messages
from error import InputError
from error import AccessError
import auth
import channels
import message
import other
import pytest
import random
import string

def create_test_channel():
    '''
    create test channel for messages
    '''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("newvalidemail@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("newvalidemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel_invite(result["token"], channel_id["channel_id"], result1["u_id"])

    return (result, result1, channel_id)

def test_valid_search():
    result, result1, channel_id = create_test_channel()
    
    message.message_send(result, channel_id, "hello")
    
