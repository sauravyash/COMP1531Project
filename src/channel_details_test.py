############################# Channel Details Tests ###########################
import pytest

from error import AccessError
from error import InputError

from channel import channel_details
from channel import channel_invite

import auth
import channels
import other

# ----- Success Details
def test_details_simple():
    
    other.clear()
    
    # Register and login a user.
    auth.auth_register('validemail@gmail.com', 'password123', 'fname', 'lname')
    result = auth.auth_login('validemail@gmail.com', 'password123')
    
    # Create a channel with this user.
    channel_id = channels.channels_create(result['token'], 'channel_1', True)
    
    # Check this user can access the channel's details.
    details = channel_details(result['token'], channel_id['channel_id'])
    assert details == {
        'name': 'channel_1',
        'owner_members': [1],
        'all_members': [1],
    }

def test_details_big():
    
    other.clear()
    
    # Register and login three users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    result1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    result2 = auth.auth_login('validemail2@gmail.com', 'password123')
    
    auth.auth_register('validemail3@gmail.com', 'password123', 'fname3', 'lname3')
    result3 = auth.auth_login('validemail3@gmail.com', 'password123')
    
    # Create a channel with the first user.
    channel_id = channels.channels_create(result1['token'], 'channel_1', True)
    
    # Invite the second user to the channel.
    channel_invite(result1['token'], channel_id['channel_id'], result2['u_id'])
    
    result_details = {
        'name': 'channel_1',
        'owner_members': [1],
        'all_members': [1, 2],
    }
    # Check the first user can access the channel's details.
    assert channel_details(result1['token'], channel_id['channel_id']) == result_details
    # Check the second user can also access these details.
    assert channel_details(result2['token'], channel_id['channel_id']) == result_details
    # Check the third user doesn not have access to details.
    with pytest.raises(AccessError):
        channel_details(result3['token'], channel_id['channel_id'])

# ----- Fail Details
def test_not_member():
    
    other.clear()
    
    # Register and login two users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    result1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    result2 = auth.auth_login('validemail2@gmail.com', 'password123')
    
    # Create a channel with the first user.
    channel_id = channels.channels_create(result1['token'], 'channel_1', True)
    
    # Test that second user is not able to access channel details.
    with pytest.raises(AccessError):
        channel_details(result2['token'], channel_id['channel_id'])

def test_invalid_token():
    
    other.clear()
    
    # Register and login a user.
    auth.auth_register('validemail@gmail.com', 'password123', 'fname', 'lname')
    result = auth.auth_login('validemail@gmail.com', 'password123')
    
    # Create a channel with first user.
    channel_id = channels.channels_create(result['token'], 'channel_1', True)
    
    # Check that Access Error is raised when invalid token is used.
    with pytest.raises(AccessError):
        channel_details('fake_token', channel_id['channel_id'])

def test_invalid_channel():

    other.clear()
    
    # Register and login a user.
    auth.auth_register('validemail@gmail.com', 'password123', 'fname', 'lname')
    result = auth.auth_login('validemail@gmail.com', 'password123')
    
    # Create a channel with first user.
    channels.channels_create(result['token'], 'channel_1', True)
    
    # Check that Input Error is raised when invalid channel is used.
    with pytest.raises(InputError):
        channel_details(result['token'], -1)

