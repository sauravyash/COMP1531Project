''' Import Functions '''
import random
import string
import pytest
import other
import auth
import channels
import channel
from error import InputError, AccessError
from standup import standup_start

def test_standup_start_success():
    ''' Success standup start case'''
    other.clear()

    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("coolemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    assert (isinstance(standup_start(result["token"], channel_id["channel_id"], 100), float))


def test_invalid_channel_id():
    '''When the standup is started to an invalid channel ID'''
    other.clear()

    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("coolemail@gmail.com", "password123")

    channels.channels_create(result["token"], "channel_1", True)

    with pytest.raises(InputError):
        standup_start(result["token"], -999, 100)

def test_standup_exists():
    '''When the standup already exists'''
    other.clear()

    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("coolemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    standup_start(result["token"],channel_id["channel_id"],100)

    with pytest.raises(InputError):
        standup_start(result["token"],channel_id["channel_id"],1)
