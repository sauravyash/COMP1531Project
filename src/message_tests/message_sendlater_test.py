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
from testing_fixtures.message_test_fixtures import setup_test_interface

def test_message_sendlater_success(setup_test_interface):
    ''' Success message sendlater case'''
    user1, _, _, channel_dict = setup_test_interface

    tok1 = user1['token']
    channel_id = channel_dict['channel_id']

    send_time = dt.datetime(2020, 11, 11, 8, 0)

    return_value = message_sendlater(tok1, channel_id, "Hello There!", send_time)
    assert isinstance(return_value, int)


def test_invalid_channel_id(setup_test_interface):
    '''When the message sent to an invalid channel ID'''
    user1, _, _, _ = setup_test_interface

    tok1 = user1['token']


    send_time = dt.datetime(2020, 11, 11, 9, 30)

    with pytest.raises(InputError):
        message_sendlater(tok1, 999, "Funky Monkey", send_time)


def test_exceed_word_limit(setup_test_interface):
    '''When the message exceeds 1000 words'''
    user1, _, _, channel_dict = setup_test_interface

    tok1 = user1['token']
    channel_id = channel_dict['channel_id']

    send_time = dt.datetime(2020, 11, 11, 9, 30)

    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(1005))

    with pytest.raises(InputError):
        message_sendlater(tok1, channel_id, result_str, send_time)


def test_invalid_time(setup_test_interface):
    '''When the time is already passed'''
    user1, _, _, channel_dict = setup_test_interface

    tok1 = user1['token']
    channel_id = channel_dict['channel_id']

    send_time = dt.datetime(2000, 9, 11, 8, 0)

    with pytest.raises(InputError):
        message_sendlater(tok1, channel_id, "Stay safe next year!", send_time)

def test_not_authorized(setup_test_interface):
    '''When the sender is not in the channel'''
    user1, _, _, channel_dict = setup_test_interface

    tok1 = user1['token']
    channel_id = channel_dict['channel_id']

    send_time = dt.datetime(2020, 11, 11, 9, 30)

    with pytest.raises(AccessError):
        message_sendlater(tok1, channel_id, "Not in channel", send_time)
