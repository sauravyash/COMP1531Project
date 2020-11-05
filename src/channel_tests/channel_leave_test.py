############################## Channel Leave Tests ############################
'''
Functions to test channel_leave functionality
'''
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

from testing_fixtures.channel_test_fixtures import setup_test_interface

# ----- Success Leave
def test_leave_member(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface
    
    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    # Add second user to channel
    channel_join(tok2, channel_id)

    # Check that second user leaves channel.
    assert len(channel_details(tok1, channel_id)['all_members']) == 2
    assert channel_leave(tok2, channel_id) == {}
    assert len(channel_details(tok1, channel_id)['all_members']) == 1

def test_leave_owner(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface
    
    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    # Add second user to channel
    channel_join(tok2, channel_id)

    # Check that second user leaves channel.
    assert len(channel_details(tok1, channel_id)["all_members"]) == 2
    assert channel_leave(tok1, channel_id) == {}
    assert len(channel_details(tok2, channel_id)["all_members"]) == 1

# ----- Fail Leave
def test_not_member(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface
    
    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    # Test that second user is not a member of channel- cannot become owner.
    with pytest.raises(AccessError):
        channel_leave(tok2, channel_id)

def test_invalid_token(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface
    
    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    # Check that Access Error is raised when invalid token is used.
    with pytest.raises(AccessError):
        channel_leave('fake_token', channel_id)

def test_invalid_channel(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface
    
    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    # Invite the second user to the channel.
    channel_invite(tok1, channel_id, uid2)

    # Check that Input Error is raised when invalid channel is used.
    with pytest.raises(InputError):
        channel_leave(tok2, -1)
