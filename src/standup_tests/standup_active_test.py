''' Import Functions '''
''' Won't work yet as standup doesn't exist.
import datetime as dt
import random
import string
import pytest
import other
import auth
import channels
import channel
from error import InputError, AccessError
from standup import standup_active, standup_start

def test_standup_active_success():
    # Success standup active case
    other.clear()

    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("coolemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)


    #In this sucess case, there is no active standup.
    result_standup_active = standup_active(result["token"],channel_id["channel_id"])

    assert result_standup_active == {
        'is_active': False,
        'time_finish': None
    }


def test_invalid_channel_id():
    # When the standup is started to an invalid channel ID
    other.clear()

    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("coolemail@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    standup_start(result["token"],channel_id["channel_id"],100)

    with pytest.raises(InputError):
        standup_active(result["token"], -999)
'''
