'''
import functions
'''
import pytest
import auth
import channels
import other
from channel import channel_invite
from error import InputError
from error import AccessError

from message import message_send
from message import message_remove
from testing_fixtures.message_test_fixtures import setup_test_interface

def test_valid_message_remove(setup_test_interface):
    '''
    Success Messages Remove
    Remove must be from owner of the channel or sender of the message
    Owner/Sender token must be valid
    Channel id must be valid
    '''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    message_send(tok1, channel_id, "Hello")
    m_id = message_send(tok1, channel_id, "Funky Monkey")
    assert message_remove(tok1, m_id["message_id"]) == {}

def test_valid_message_remove_channel_owner(setup_test_interface):
    '''
    message remove from the channel owner
    '''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    channel_invite(tok1, channel_id, uid2)

    m_id = message_send(tok2, channel_id, "Funky Monkey")
    assert message_remove(tok1, m_id["message_id"]) == {}

def test_valid_message_remove_flockr_owner(setup_test_interface):
    '''
    the message is removed
    '''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    message_send(tok1, channel_id, "Hello")
    m_id = message_send(tok1, channel_id, "Funky Monkey")
    assert message_remove(tok1, m_id["message_id"]) == {}


def test_invalid_message_token(setup_test_interface):
    '''
    Fail
    When the token is Invalid
    '''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    message_send(tok1, channel_id, "Hello")
    m_id = message_send(tok1, channel_id, "Funky Monkey")
    with pytest.raises(AccessError):
        message_remove("Invalid token", m_id["message_id"])


def test_invalid_message_id(setup_test_interface):
    '''
    When the message id is invalid
    '''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    message_send(tok1, channel_id, "Hello")
    message_send(tok1, channel_id, "Funky Monkey")
    with pytest.raises(InputError):
        message_remove(tok1, 123)

def test_invalid_message_removed(setup_test_interface):
    '''
    When the message is already removed
    '''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    message_send(tok1, channel_id, "Hello")
    m_id = message_send(tok1, channel_id, "Funky Monkey")
    message_remove(tok1, m_id["message_id"])

    with pytest.raises(InputError):
        message_remove(tok1, m_id["message_id"])


def test_invalid_message_remove_not_sender(setup_test_interface):
    '''
    When the remove is not from the sender
    '''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    message_send(tok1, channel_id, "Edit next message")
    m_id = message_send(tok1, channel_id, "Funky Monkey")

    with pytest.raises(AccessError):
        message_remove(tok2, m_id["message_id"])


def test_invalid_message_remove_not_authorized(setup_test_interface):
    '''
    When the remove is not from owner of the channel
    '''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    m_id = message_send(tok1, channel_id, "Funky Monkey")
    with pytest.raises(AccessError):
        message_remove(tok2, m_id["message_id"])
