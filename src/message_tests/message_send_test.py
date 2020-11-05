'''
import functions
'''
import random
import string
import pytest
import auth
import channel
import channels
import other
from error import InputError
from error import AccessError

from message import message_send
from testing_fixtures.message_test_fixtures import setup_test_interface

def test_valid_message_send(setup_test_interface):
    '''
    Sender Token must be valid
    Sender must be a member of the channel
    channel id must be valid
    message letters must be within 1000 characters
    '''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    message_send(tok1, channel_id, "Funky Monkey")
    msgs = channel.channel_messages(tok1, channel_id, 0)

    assert msgs["messages"][0]['message'] == "Funky Monkey"


def test_invalid_message_token(setup_test_interface):
    '''
    When the sender token is not valid
    '''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    with pytest.raises(AccessError):
        message_send("Dodge", channel_id, "Funky Monkey")


def test_invalid_message_channel_id(setup_test_interface):
    '''
    When the message sent to an invalid channel ID
    '''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    with pytest.raises(InputError):
        message_send(tok1, 125, "Funky Monkey")

def test_invalid_message_string_size_1000(setup_test_interface):
    '''
    When the message exceeds 1000 character limit
    '''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(1005))
    with pytest.raises(InputError):
        message_send(tok1, channel_id, result_str)


def test_invalid_message_not_in_channel(setup_test_interface):
    '''
    When the sender is not a member of the channel
    '''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channels.channels_create(tok1, "channel_1", False)['channel_id']

    with pytest.raises(AccessError):
        message_send(tok2, channel_id, "Not in channel")
