############################### Channel Join Tests ############################
'''
Functions to test channel_join functionality
'''
import pytest

from error import InputError
from error import AccessError

from channel import channel_join
from channel import channel_invite

import auth
import channels
import other

from testing_fixtures.channel_test_fixtures import setup_test_interface

# ----- Success Join
def test_join_public(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    # When any member joins a public channel, they should be able to:
    # -- Firstly, the flockr owner should be able to join.
    assert channel_join(tok1, channel_id) == {}
    
    # -- Secondly, a non-flockr owner should be able to join.
    assert channel_join(tok3, channel_id) == {}

def test_join_private_owner(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    # The flockr owner can join a private channel.
    assert channel_join(tok1, channel_id) == {}

# ----- Fail Join
def test_join_private_member(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channels.channels_create(tok1, 'channel_1', False)['channel_id']

    with pytest.raises(AccessError):
        channel_join(tok2, channel_id)

def test_invalid_channel(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    # Input error is raised when fake channel is used.
    with pytest.raises(InputError):
        channel_join(tok2, -1)

def test_invalid_token(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1['token']
    tok2 = user2['token']
    uid2 = user2['u_id']
    tok3 = user3['token']
    channel_id = channel_dict['channel_id']

    # Access error is raised when a fake token is used.
    with pytest.raises(AccessError):
        channel_join('fake_token', channel_id)
