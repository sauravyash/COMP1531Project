############################### Channel Join Tests ############################
import pytest

from error import InputError
from error import AccessError

from channel import channel_join
from channel import channel_invite

import auth
import channels
import other

# ----- Success Join
def test_join_public():
    
    other.clear()
    
    # Register and login three users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    result1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    result2 = auth.auth_login('validemail2@gmail.com', 'password123')
    
    auth.auth_register('validemail3@gmail.com', 'password123', 'fname3', 'lname3')
    result3 = auth.auth_login('validemail3@gmail.com', 'password123')
    
    # Create a channel with the second user.
    channel_id = channels.channels_create(result2['token'], 'channel_1', True)
    
    # When any member joins a public channel, they should be able to:
    # -- Firstly, the flockr owner should be able to join.
    assert channel_join(result1['token'], channel_id['channel_id']) == {}
    # -- Secondly, a non-flockr owner should be able to join.
    assert channel_join(result3['token'], channel_id['channel_id']) == {}

def test_join_private_owner():
    
    other.clear()
    
    # Register and login two users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    result1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    result2 = auth.auth_login('validemail2@gmail.com', 'password123')
    
    # Create a channel with the first user.
    channel_id = channels.channels_create(result2['token'], 'channel_1', False)
    
    # The flockr owner can join a private channel.
    assert channel_join(result1['token'], channel_id['channel_id']) == {}

# ----- Fail Join
def test_join_private_member():
    
    other.clear()
    
    # Register and login two users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    result1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    result2 = auth.auth_login('validemail2@gmail.com', 'password123')
    
    # Create a channel with the first user.
    channel_id = channels.channels_create(result1['token'], 'channel_1', False)
    
    with pytest.raises(AccessError):
        channel_join(result2['token'], channel_id['channel_id'])

def test_invalid_channel():
    
    other.clear()
    
    # Register and login two users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    result1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    result2 = auth.auth_login('validemail2@gmail.com', 'password123')
    
    # Create a channel with first user.
    channels.channels_create(result1['token'], 'channel_1', True)
    
    # Input error is raised when fake channel is used.
    with pytest.raises(InputError):
        channel_join(result2['token'], -1)
        
def test_invalid_token():
    
    other.clear()
    
    # Register and login a user.
    auth.auth_register('validemail@gmail.com', 'password123', 'fname', 'lname')
    result = auth.auth_login('validemail@gmail.com', 'password123')
    
    # Create a channel with first user.
    channel_id = channels.channels_create(result['token'], 'channel_1', True)
    
    # Access error is raised when a fake token is used.
    with pytest.raises(AccessError):
        channel_join('fake_token', channel_id['channel_id'])
