###############################Channel Invite Tests#############################
import pytest

from error import InputError
from error import AccessError

from channel import channel_invite
import auth
import channels
import other

# ----- Success Invite
def test_valid_invite_p1():
    
    other.clear()
    
    # Register and login two users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    result1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    result2 = auth.auth_login('validemail2@gmail.com', 'password123')
    
    # Create a channel with the first user.
    channel_id = channels.channels_create(result1['token'], 'channel_1', True)
    
    # Check that second user can be added by first user.
    assert channel_invite(result1['token'], channel_id['channel_id'], result2['u_id']) == {}
    
def test_valid_invite_p2():
    
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
    
    # Check that second user can be added by first user (the owner).
    assert channel_invite(result1['token'], channel_id['channel_id'], result2['u_id']) == {}
    # Now check that the thrid user can be added by the second user (a member).
    assert channel_invite(result2['token'], channel_id['channel_id'], result3['u_id']) == {}

# ----- Fail Invite
def test_invite_oneself():
    
    other.clear()
    
    # Register and login two users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    result1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    result2 = auth.auth_login('validemail2@gmail.com', 'password123')
    
    # Create a channel with first user.
    channel_id = channels.channels_create(result1['token'], 'channel_1', True)
    
    # Second user attempts to invite themself and should raise Access Error.
    with pytest.raises(AccessError):
        channel_invite(result2['token'], channel_id['channel_id'], result2['u_id'])

def test_invalid_token():
    
    other.clear()
    
    # Register and login a user.
    auth.auth_register('validemail@gmail.com', 'password123', 'fname', 'lname')
    result = auth.auth_login('validemail@gmail.com', 'password123')
    
    # Create a channel with first user.
    channel_id = channels.channels_create(result['token'], 'channel_1', True)
    
    # Access error is raised when a fake token is used.
    with pytest.raises(AccessError):
        channel_invite('fake_token', channel_id['channel_id'], result['u_id'])

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
        channel_invite(result1['token'], -1, result2['u_id'])

def test_invalid_user_id():
    
    other.clear()
    
    # Register and login one user.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    result1 = auth.auth_login('validemail1@gmail.com', 'password123')
    
    # Create a channel with first user.
    channel_id = channels.channels_create(result1['token'], 'channel_1', True)
    
    # Input error is raised when fake user ID is used.
    with pytest.raises(InputError):
        channel_invite(result1['token'], channel_id['channel_id'], -1)

