############################## Channel Leave Tests ############################
import pytest

from error import InputError
from error import AccessError

from channel import channel_invite
from channel import channel_leave
from channel import channel_join
from channel import channel_details

import auth
import channels
import other

# ----- Success Leave
def test_leave_member():
    
    other.clear()
    
    # Register and login two users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    result1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    result2 = auth.auth_login('validemail2@gmail.com', 'password123')
    
    # Create a channel with first user.
    channel_id = channels.channels_create(result1['token'], 'channel_1', True)
    
    # Add second user to channel
    channel_join(result2['token'], channel_id['channel_id'])
    
    # Result data:
    data_before = {
        'name': 'channel_1',
        'owner_members': [1],
        'all_members': [1, 2],
    }
    data_after = {
        'name': 'channel_1',
        'owner_members': [1],
        'all_members': [1],
    }
    
    # Check that second user leaves channel.
    assert channel_details(result1['token'], channel_id['channel_id']) == data_before
    assert channel_leave(result2['token'], channel_id['channel_id']) == {}
    assert channel_details(result1['token'], channel_id['channel_id']) == data_after

def test_leave_owner():
    
    other.clear()
    
    # Register and login two users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    result1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    result2 = auth.auth_login('validemail2@gmail.com', 'password123')
    
    # Create a channel with first user.
    channel_id = channels.channels_create(result1['token'], 'channel_1', True)
    
    # Add second user to channel
    channel_join(result2['token'], channel_id['channel_id'])
    
    # Result data:
    data_before = {
        'name': 'channel_1',
        'owner_members': [1],
        'all_members': [1, 2],
    }
    data_after = {
        'name': 'channel_1',
        'owner_members': [],
        'all_members': [2],
    }
    
    # Check that second user leaves channel.
    assert channel_details(result1['token'], channel_id['channel_id']) == data_before
    assert channel_leave(result1['token'], channel_id['channel_id']) == {}
    assert channel_details(result2['token'], channel_id['channel_id']) == data_after

# ----- Fail Leave
def test_not_member():
    
    other.clear()
    
    # Register and login two users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    result1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    result2 = auth.auth_login('validemail2@gmail.com', 'password123')
    
    # Create a channel with the first user.
    channel_id = channels.channels_create(result1['token'], 'channel_1', True)
    
    # Test that second user is not a member of channel- cannot become owner.
    with pytest.raises(AccessError):
        channel_leave(result2['token'], channel_id['channel_id'])

def test_invalid_token():
    
    other.clear()
    
    # Register and login two users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    result1 = auth.auth_login('validemail1@gmail.com', 'password123')
    
    # Create a channel with first user.
    channel_id = channels.channels_create(result1['token'], 'channel_1', True)
    
    # Check that Access Error is raised when invalid token is used.
    with pytest.raises(AccessError):
        channel_leave('fake_token', channel_id['channel_id'])

def test_invalid_channel():

    other.clear()
    
    # Register and login two users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    result1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    result2 = auth.auth_login('validemail2@gmail.com', 'password123')
    
    # Create a channel with first user.
    channel_id = channels.channels_create(result1['token'], 'channel_1', True)
    
    # Invite the second user to the channel.
    channel_invite(result1['token'], channel_id['channel_id'], result2['u_id'])
    
    # Check that Input Error is raised when invalid channel is used.
    with pytest.raises(InputError):
        channel_leave(result2['token'], -1)
