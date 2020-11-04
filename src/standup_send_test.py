''' Import Functions '''
import random
import string
import pytest
import other
import auth
import channels
import channel
from error import InputError, AccessError
from standup import standup_send, standup_active, standup_start

def test_standup_active_success():
    ''' Success standup send case'''
    other.clear()

    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("coolemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    standup_start(result["token"], channel_id["channel_id"], 100)

    assert (standup_send(result["token"], channel_id["channel_id"], "General Kenobi")) == {}


def test_invalid_channel_id():
    '''When the standup message is sent to an invalid channel ID'''
    other.clear()

    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("coolemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    standup_start(result["token"],channel_id["channel_id"],1)

    with pytest.raises(InputError):
        standup_send(result["token"], -999, "General Kenobi")

def test_invalid_message_string_size():
    '''When the standup message exceeds 1000 characters'''
    other.clear()
    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("coolemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    standup_start(result["token"],channel_id["channel_id"],100)

    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(1005))

    with pytest.raises(InputError):
        standup_send(result["token"], channel_id["channel_id"], result_str)

def test_inactive_standup():
    '''When the standup is inactive and a message is sent'''
    other.clear()

    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("coolemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    with pytest.raises(InputError):
        standup_send(result["token"], channel_id["channel_id"], "General Kenobi")

def test_non_member_channel():
    '''Non-member of the channel'''
    other.clear()

    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("coolemail@gmail.com", "password123")

    auth.auth_register("goodemail@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("goodemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    standup_start(result["token"], channel_id["channel_id"], 1)

    with pytest.raises(AccessError):
        standup_send(result1["token"], channel_id["channel_id"], "General Kenobi")
