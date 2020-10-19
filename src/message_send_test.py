'''
import functions
'''
import random
import string
import pytest
import auth
import channels
import other
from error import InputError
from error import AccessError
# assume message id is an int
from message import message_send

def create_test_channel():
    '''
    Create test channel for message send
    '''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    return (result, channel_id)

# Success Messages

def test_valid_message_send():
    '''
    Sender Token must be valid
    Sender must be a member of the channel
    channel id must be valid
    message letters must be within 1000 characters
    '''
    result, channel_id = create_test_channel()
    message_send(result["token"], channel_id["channel_id"], "Funky Monkey")

# Fail
def test_invalid_message_token():
    '''
    When the sender token is not valid
    '''
    #other.clear
    auth.auth_register("cool_email@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("cool_email@gmail.com", "password123")

    auth.auth_register("good_email@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("good_email@gmail.com", "password123")
    channel_id = channels.channels_create(result["token"], "channel_1", True)

    with pytest.raises(InputError):
        message_send("Dodge", channel_id["channel_id"], "Funky Monkey")

# When the message sent to an invalid channel
def test_invalid_message_channel_id():
    '''
    When the message sent to an invalid channel ID
    '''
    #other.clear
    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("coolemail@gmail.com", "password123")
    channels.channels_create(result["token"], "channel_1", True)
    with pytest.raises(InputError):
        message_send(result["token"], 125, "Funky Monkey")

def test_invalid_message_string_size_1000():
    '''
    When the message exceeds 1000 character limit
    '''

    result, channel_id = create_test_channel()
    # Generate message exceeds 1000 on purpose
    # remove when implementation is complete
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(1005))
    with pytest.raises(InputError):
        message_send(result["token"], channel_id["channel_id"], result_str)


def test_invalid_message_not_in_channel():
    '''
    When the sender is not a member of the channel
    '''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("good_email@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("good_email@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", False)

    # Not invited to the channel

    with pytest.raises(AccessError):
        message_send(result1["token"], channel_id["channel_id"], "Not in channel")
