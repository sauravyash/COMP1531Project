''' Import Functions '''
import datetime as dt
import random
import string
import pytest
import other
import auth
import channels
from error import InputError, AccessError
from message import message_sendlater

def test_message_sendlater_success():
    ''' Success message sendlater case'''
    other.clear()

    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("coolemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    send_time = dt.datetime(2020, 11, 11, 8, 0).timestamp()

    return_value = message_sendlater(result["token"], channel_id['channel_id'], "Hello There!", send_time)
    assert isinstance(return_value['message_id'], int)


def test_invalid_channel_id():
    '''When the message sent to an invalid channel ID'''
    other.clear()

    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("coolemail@gmail.com", "password123")

    channels.channels_create(result["token"], "channel_1", True)

    send_time = dt.datetime(2020, 11, 11, 9, 30).timestamp()

    with pytest.raises(InputError):
        message_sendlater(result["token"], 999, "Funky Monkey", send_time)


def test_exceed_word_limit():
    '''When the message exceeds 1000 words'''
    other.clear()

    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("coolemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    send_time = dt.datetime(2020, 11, 11, 9, 30).timestamp()

    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(1005))

    with pytest.raises(InputError):
        message_sendlater(result["token"], channel_id['channel_id'], result_str, send_time)


def test_invalid_time():
    '''When the time is already passed'''
    other.clear()

    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("coolemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    send_time = dt.datetime(2000, 9, 11, 8, 0).timestamp()

    with pytest.raises(InputError):
        message_sendlater(result["token"], channel_id['channel_id'], "Stay safe next year!", send_time)


def test_not_authorized():
    '''When the sender is not in the channel'''
    other.clear()

    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("good_email@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("good_email@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    send_time = dt.datetime(2020, 11, 11, 9, 30).timestamp()

    with pytest.raises(AccessError):
        message_sendlater(result1["token"], channel_id['channel_id'], "Not in channel", send_time)
