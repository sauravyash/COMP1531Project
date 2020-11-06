############################ Channel Removeowner Tests ########################
'''
Functions to test channel_removeowner functionality
'''
import pytest

from error import AccessError
from error import InputError

from channel import channel_invite
from channel import channel_removeowner
from channel import channel_addowner
from channel import channel_details

import auth
import channels
import other

# ----- Success Removeowner
def test_addowner_simple():

    other.clear()

    # Register and login two users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    result1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    result2 = auth.auth_login('validemail2@gmail.com', 'password123')

    # Create a channel with the first user.
    channel_id = channels.channels_create(result1['token'], 'channel_1', True)

    # Invite the second user to the channel.
    channel_invite(result1['token'], channel_id['channel_id'], result2['u_id'])

    # Add the second user as an owner.
    assert channel_addowner(result1['token'], channel_id['channel_id'], result2['u_id']) == {}

    # Check that second user's owner status is removed.
    assert len(channel_details(result1['token'], channel_id['channel_id'])['owner_members']) == 2
    assert channel_removeowner(result1['token'], channel_id['channel_id'], result2['u_id']) == {}
    assert len(channel_details(result1['token'], channel_id['channel_id'])['owner_members']) == 1

def test_flockr_owner():

    other.clear()

   # Register and login three users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    result1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    result2 = auth.auth_login('validemail2@gmail.com', 'password123')

    auth.auth_register('validemail3@gmail.com', 'password123', 'fname3', 'lname3')
    result3 = auth.auth_login('validemail3@gmail.com', 'password123')

    # Create a channel with the first user.
    channel_id = channels.channels_create(result2['token'], 'channel_1', True)

    # Invite the second user to the channel.
    channel_invite(result2['token'], channel_id['channel_id'], result1['u_id'])
    channel_invite(result2['token'], channel_id['channel_id'], result3['u_id'])

    # Second user (owner of channel) adds third user as a channel owner.
    assert channel_addowner(result2['token'], channel_id['channel_id'], result3['u_id']) == {}

    # Check that flockr owner can also remove a channel owner.
    assert len(channel_details(result2['token'], channel_id['channel_id'])["owner_members"]) == 2
    assert channel_removeowner(result3['token'], channel_id['channel_id'], result2['u_id']) == {}
    assert len(channel_details(result3['token'], channel_id['channel_id'])["owner_members"]) == 1


# ----- Fail Removeowner
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
    with pytest.raises(InputError):
        channel_removeowner(result1['token'], channel_id['channel_id'], result2['u_id'])

def test_invalid_token():

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

    # Check that Access Error is raised when invalid token is used.
    with pytest.raises(AccessError):
        channel_removeowner('fake_token', channel_id['channel_id'], result2['u_id'])

def test_invalid_user_id():

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

    # Check that Access Error is raised when invalid token is used.
    with pytest.raises(InputError):
        channel_removeowner('fake_token', channel_id['channel_id'], -1)

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
        channel_removeowner(result1['token'], -1, result2['u_id'])

def test_not_authorized():

    other.clear()

    # Register and login three users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    result1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    result2 = auth.auth_login('validemail2@gmail.com', 'password123')

    auth.auth_register('validemail3@gmail.com', 'password123', 'fname3', 'lname3')
    result3 = auth.auth_login('validemail3@gmail.com', 'password123')

    # Create a channel with first user.
    channel_id = channels.channels_create(result1['token'], 'channel_1', True)

    # Invite the second & third users to the channel.
    channel_invite(result1['token'], channel_id['channel_id'], result2['u_id'])
    channel_invite(result2['token'], channel_id['channel_id'], result3['u_id'])

    # Second member (not owner) tries to remove first member (owner)- raise Access Error.
    with pytest.raises(AccessError):
        channel_removeowner(result2['token'], channel_id['channel_id'], result1['u_id'])

def test_not_owner():

    other.clear()

    # Register and login three users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    result1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    result2 = auth.auth_login('validemail2@gmail.com', 'password123')

    auth.auth_register('validemail3@gmail.com', 'password123', 'fname3', 'lname3')
    result3 = auth.auth_login('validemail3@gmail.com', 'password123')

    # Create a channel with first user.
    channel_id = channels.channels_create(result1['token'], 'channel_1', True)

    # Invite the second & third users to the channel.
    channel_invite(result1['token'], channel_id['channel_id'], result2['u_id'])
    channel_invite(result2['token'], channel_id['channel_id'], result3['u_id'])

    # First member (owner) tries to remove second member (not owner)- raise Input Error.
    with pytest.raises(InputError):
        channel_removeowner(result1['token'], channel_id['channel_id'], result2['u_id'])
