'''Import functions'''
import pytest
import auth
import channel
import channels
import other
from error import InputError
from error import AccessError
from message import message_send, message_react, message_unreact
from testing_fixtures.message_test_fixtures import setup_test_interface

def test_success_unreact(setup_test_interface):
    ''' Success message unreact case'''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    m_id = message_send(tok1, channel_id, "Funky Monkey")

    message_react(tok1, m_id["message_id"], 1)

    assert (message_unreact(tok1, m_id["message_id"], 1)) == {}


def test_invalid_message_id(setup_test_interface):
    '''Invalid message ID'''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    m_id = message_send(tok1, channel_id, "Funky Monkey")

    message_react(tok1, m_id["message_id"], 1)

    with pytest.raises(InputError):
        message_unreact(tok1, -999, 1)

def test_invalid_unreact_id(setup_test_interface):
    '''Invalid message react ID'''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    m_id = message_send(tok1, channel_id, "Funky Monkey")

    message_react(tok1, m_id["message_id"], 1)

    with pytest.raises(InputError):
        message_unreact(tok1, m_id["message_id"], -999)
        

def test_no_react(setup_test_interface):
    '''No react'''
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    m_id = message_send(tok1, channel_id, "Funky Monkey")

    with pytest.raises(InputError):
        message_unreact(tok1, m_id["message_id"], 1)
