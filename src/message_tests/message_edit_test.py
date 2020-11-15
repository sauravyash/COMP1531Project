'''
import functions
'''
import random
import string
import pytest
import other
import auth
import channels
import channel
from error import InputError, AccessError
'''assume message id is an int'''
from message import message_send, message_edit
from testing_fixtures.message_test_fixtures import setup_test_interface

def test_valid_message_edit(setup_test_interface):
    '''
    Success Messages
    Valid sender token
    Valid message ID
    Edited message within 1000 charactre limit
    Edit authorized by owner or sender
    '''
    user1, _, _, channel_dict = setup_test_interface

    tok1 = user1['token']
    channel_id = channel_dict['channel_id']
 
    m_id = message_send(tok1, channel_id, "Funky Monkey")
    assert message_edit(tok1, m_id["message_id"], "Monkey Funky") == {}
    msgs = channel.channel_messages(tok1, channel_id, 0)

    assert msgs["messages"][0]['message'] == "Monkey Funky"

def test_authorized_edit_owner(setup_test_interface):
    '''
    Success Messages
    Valid sender token
    Valid message ID
    Edited message within 1000 charactre limit
    Edit authorized by owner or sender
    '''
    user1, user2, _, channel_dict = setup_test_interface

    tok1 = user1['token']
    uid1 = user1['u_id']
    tok2 = user2['token']
    uid2 = user2['u_id']
    channel_id = channel_dict['channel_id']

    channel.channel_invite(tok1, channel_id, uid2)
    channel.channel_invite(tok1, channel_id, uid1)
    m_id = message_send(tok2, channel_id, "Funky Monkey")
    assert message_edit(tok1, m_id["message_id"], "Monkey Funky") == {}

def test_authorized_edit_flockr_owner(setup_test_interface):
    '''
    Authorized from the owner of the flockr
    '''
    user1, _, _, channel_dict = setup_test_interface

    tok1 = user1['token']
    channel_id = channel_dict['channel_id']

    m_id = message_send(tok1, channel_id, "Funky Monkey")
    assert message_edit(tok1, m_id["message_id"], "Monkey Funky") == {}


'''Fail'''
def test_invalid_token(setup_test_interface):
    '''
    Invalid sender/owner token
    '''
    user1, _, _, channel_dict = setup_test_interface

    tok1 = user1['token']
    channel_id = channel_dict['channel_id']

    message_send(tok1, channel_id, "Hello")
    m_id = message_send(tok1, channel_id, "Funky Monkey")
    with pytest.raises(AccessError):
        message_edit("Invalid token", m_id["message_id"], "Monkey Funky")

def test_invalid_message_id(setup_test_interface):
    '''
    Invalid message ID
    '''
    user1, _, _, channel_dict = setup_test_interface

    tok1 = user1['token']
    channel_id = channel_dict['channel_id']  

    message_send(tok1, channel_id, "Hello")
    message_send(tok1, channel_id, "Funky Monkey")
    with pytest.raises(InputError):
        message_edit(tok1, -1, "Monkey Funky")

def test_invalid_message_edit_exceeds_size_limit(setup_test_interface):
    '''
    Message edit size exceeds 1000'
    '''
    user1, _, _, channel_dict = setup_test_interface

    tok1 = user1['token']
    channel_id = channel_dict['channel_id']  

    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(1005))
    m_id = message_send(tok1, channel_id, "Funky Monkey")
    with pytest.raises(InputError):
        message_edit(tok1, m_id["message_id"], result_str)

def test_invalid_message_edit_not_sender(setup_test_interface):
    '''
    Edit not from the sender
    '''
    user1, user2, _, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    channel_id = channel_dict['channel_id']  

    channel.channel_invite(tok1, channel_id, uid2)

    m_id = message_send(tok1, channel_id, "Funky Monkey")
    with pytest.raises(AccessError):
        message_edit(tok2, m_id["message_id"], "Monkey Funky")


def test_invalid_message_edit_not_authorized(setup_test_interface):
    '''
    Member trying to edit owner message
    '''
    user1, user2, _, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    channel_id = channel_dict['channel_id']  

    m_id = message_send(tok1, channel_id, "Funky Monkey")
    with pytest.raises(AccessError):
        message_edit(tok2, m_id["message_id"], "Monkey Funky")
