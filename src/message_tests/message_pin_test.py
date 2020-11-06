'''Import functions'''
import pytest
import auth
import channel
import channels
import other
from error import InputError
from error import AccessError
from message import message_send, message_pin

from testing_fixtures.message_test_fixtures import setup_test_interface

def test_success_pin(setup_test_interface):
    ''' Success message react case'''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']
   
    m_id = message_send(tok1, channel_id, "Funky Monkey")

    assert (message_pin(tok1, m_id["message_id"])) == {}


def test_invalid_message_id(setup_test_interface):
    '''Invalid message ID'''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    message_send(tok1, channel_id, "Funky Monkey")

    with pytest.raises(InputError):
        message_pin(tok1, -999)


def test_pin_already(setup_test_interface):
    '''Invalid message react ID'''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    m_id = message_send(tok1, channel_id, "Funky Monkey")

    message_pin(tok1, m_id["message_id"])

    with pytest.raises(InputError):
        message_pin(tok1, m_id["message_id"])


def test_not_in_channel(setup_test_interface):
    '''User not a member'''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    m_id = message_send(tok1, channel_id, "Funky Monkey")

    with pytest.raises(AccessError):
        message_pin(tok2, m_id["message_id"])

def test_not_owner(setup_test_interface):
    '''User not owner'''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    channel.channel_invite(tok1, channel_id, uid2)

    m_id = message_send(tok1, channel_id, "Funky Monkey")

    with pytest.raises(AccessError):
        message_pin(tok2, m_id["message_id"])
