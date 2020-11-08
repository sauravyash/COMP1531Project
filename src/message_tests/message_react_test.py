'''Import functions'''
import pytest
import auth
import channel
import channels
import other
from error import InputError
from error import AccessError
from message import message_send, message_react
from testing_fixtures.message_test_fixtures import setup_test_interface

def test_success_react(setup_test_interface):
    ''' Success message react case'''
    user1, _, _, channel_dict = setup_test_interface

    tok1 = user1['token']
    channel_id = channel_dict['channel_id']

    m_id = message_send(tok1, channel_id, "Funky Monkey")

    assert (message_react(tok1, m_id["message_id"], 1)) == {}


def test_invalid_message_id(setup_test_interface):
    '''Invalid message ID'''
    user1, _, _, channel_dict = setup_test_interface

    tok1 = user1['token']
    channel_id = channel_dict['channel_id']

    message_send(tok1, channel_id, "Funky Monkey")

    with pytest.raises(InputError):
        message_react(tok1, -1, 1)



def test_invalid_react_id(setup_test_interface):
    '''Invalid message react ID'''
    user1, _, _, channel_dict = setup_test_interface

    tok1 = user1['token']
    channel_id = channel_dict['channel_id']

    m_id = message_send(tok1, channel_id, "Funky Monkey")

    with pytest.raises(InputError):
        message_react(tok1, m_id["message_id"], -999)



def test_react_already_exist(setup_test_interface):
    '''Invalid message react ID'''
    user1, _, _, channel_dict = setup_test_interface

    tok1 = user1['token']
    channel_id = channel_dict['channel_id']

    m_id = message_send(tok1, channel_id, "Funky Monkey")

    message_react(tok1, m_id["message_id"], 1)

    with pytest.raises(InputError):
        message_react(tok1, m_id["message_id"], 1)
