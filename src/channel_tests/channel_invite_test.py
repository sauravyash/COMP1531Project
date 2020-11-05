###############################Channel Invite Tests#############################
'''
Functions to test channel_invite functionality
'''
import pytest

from error import InputError
from error import AccessError

from channel import channel_invite
import auth
import channels
import other

from testing_fixtures.channel_test_fixtures import setup_test_interface

# ----- Success Invite
def test_valid_invite_p1(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface
    
    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok2 = user3['token']
    channel_id = channel_dict['channel_id']
    
    # Check that second user can be added by first user.
    assert channel_invite(tok1, channel_id, uid2) == {}

def test_valid_invite_p2(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface
    
    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    uid3 = user3['u_id']
    channel_id = channel_dict['channel_id']
    
    # Check that second user can be added by first user (the owner).
    assert channel_invite(tok1, channel_id, uid2) == {}
    # Now check that the thrid user can be added by the second user (a member).
    assert channel_invite(tok2, channel_id, uid3) == {}

# ----- Fail Invite
def test_invite_oneself(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface
    
    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    uid3 = user3['u_id']
    channel_id = channel_dict['channel_id']

    # Second user attempts to invite themself and should raise Access Error.
    with pytest.raises(AccessError):
        channel_invite(tok2, channel_id, uid2)

def test_invalid_token(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface
    
    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    uid3 = user3['u_id']
    channel_id = channel_dict['channel_id']

    # Access error is raised when a fake token is used.
    with pytest.raises(AccessError):
        channel_invite('fake_token', channel_id, uid2)

def test_invalid_channel(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface
    
    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    uid3 = user3['u_id']
    channel_id = channel_dict['channel_id']

    # Input error is raised when fake channel is used.
    with pytest.raises(InputError):
        channel_invite(tok1, -1, uid2)

def test_invalid_user_id(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface
    
    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    uid3 = user3['u_id']
    channel_id = channel_dict['channel_id']

    # Input error is raised when fake user ID is used.
    with pytest.raises(InputError):
        channel_invite(tok1, channel_id, -1)
