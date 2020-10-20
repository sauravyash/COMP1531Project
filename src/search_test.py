from channel import channel_invite
from channel import channel_messages
from error import InputError
from error import AccessError
import auth
import channels
import message
import other
import pytest
import random
import string

def create_test_channel():
    '''
    create test channel for messages
    '''
    other.clear()
    
    # Register and login two users...
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result1 = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("newvalidemail@gmail.com", "password123", "fname1", "lname1")
    result2 = auth.auth_login("newvalidemail@gmail.com", "password123")
    
    # Create a channel and invite a user to it...
    channel = channels.channels_create(result1['token'], 'channel_1', True)
    channel_invite(result1['token'], channel['channel_id'], result2['u_id'])

    return (result1['token'], result2['token'], channel['channel_id'])

def test_simple_search():
    # Create test environment...
    token1, token2, channel_id = create_test_channel()
    
    # Send messages...
    mid_1 = message.message_send(token1, channel_id, 'hello')
    mid_2 = message.message_send(token2, channel_id, 'help me')
    mid_3 = message.message_send(token1, channel_id, 'what the hell')
    
    # Test search...
    return_messages = other.search(token1, 'he')
    print(return_messages)
    assert return_messages['messages'][1]['message_id'] == mid_1
    assert return_messages['messages'][2]['message_id'] == mid_2
    assert return_messages['messages'][3]['message_id'] == mid_3
    
def test_selective_search():
    # Create test environment...
    token1, token2, channel_id = create_test_channel()
    
    # Send messages...
    mid_1 = message.message_send(token1, channel_id, 'hello')
    message.message_send(token2, channel_id, 'help me')
    mid_3 = message.message_send(token1, channel_id, 'what the hell')
    
    # Test search...
    return_messages1 = other.search(token1, 'hell')
    assert return_messages1['messages'][1]['message_id'] == mid_1
    assert return_messages1['messages'][2]['message_id'] == mid_3
    
    return_messages2 = other.search(token1, 'what the')
    assert return_messages2['messages'][1]['message_id'] == mid_3

def test_diff_users():
    
    # Create test environment...
    token1, token2, channel_id = create_test_channel()
    
    # Send messages...
    mid_1 = message.message_send(token1, channel_id, 'hello')
    message.message_send(token2, channel_id, 'help me')
    mid_3 = message.message_send(token1, channel_id, 'what the hell')
    
    # Test search...
    return_messages1 = other.search(token1, 'hell')
    assert return_messages1['messages'][1]['message_id'] == mid_1
    assert return_messages1['messages'][2]['message_id'] == mid_3
    
    return_messages2 = other.search(token2, 'hell')
    assert return_messages2['messages'][1]['message_id'] == mid_1
    assert return_messages2['messages'][2]['message_id'] == mid_3
    
    assert other.search('fake_token', 'hell') == {'messages': []}

