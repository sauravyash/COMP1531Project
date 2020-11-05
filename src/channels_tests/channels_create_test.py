############################ Channel Create Tests #############################
'''
Functions to test channels_create functionality
'''

import pytest
import other
import auth

from error import InputError
from error import AccessError

from channels import channels_create
import channel

@pytest.fixture()
def setup_test_interface():
    other.clear()

    # Register and login two users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    user1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    user2 = auth.auth_login('validemail2@gmail.com', 'password123')

    return user1['token'], user2['token']

# ----- Success Create
def test_simple(setup_test_interface):
    user1, _ = setup_test_interface

    channel_1 = channels_create(user1, "channel_1", True)['channel_id']
    assert len(channel.channel_details(user1, channel_1)['owner_members']) == 1
    assert len(channel.channel_details(user1, channel_1)['all_members']) == 1

    channel_2 = channels_create(user1, "channel_2", False)['channel_id']
    assert len(channel.channel_details(user1, channel_2)['owner_members']) == 1
    assert len(channel.channel_details(user1, channel_2)['all_members']) == 1

def test_multiple_users(setup_test_interface):
    user1, user2 = setup_test_interface

    channel_1 = channels_create(user1, "channel_1", True)['channel_id']
    assert len(channel.channel_details(user1, channel_1)['owner_members']) == 1
    assert len(channel.channel_details(user1, channel_1)['all_members']) == 1

    channel_2 = channels_create(user2, "channel_2", False)['channel_id']
    assert len(channel.channel_details(user2, channel_2)['owner_members']) == 1
    assert len(channel.channel_details(user2, channel_2)['all_members']) == 1

# ----- Fail Create
def test_invalid_token(setup_test_interface):
    setup_test_interface

    with pytest.raises(AccessError):
        channels_create(0, "channel_id", True)
    with pytest.raises(AccessError):
        channels_create("", "channel_id", True)
    with pytest.raises(AccessError):
        channels_create(None, "channel_id", True)

def test_invalid_channel_name(setup_test_interface):
    user1, _ = setup_test_interface

    with pytest.raises(InputError):
        assert channels_create(user1, None, True)
    with pytest.raises(InputError):
        assert channels_create(user1, "", True)
    with pytest.raises(InputError):
        # 21 char length name
        assert channels_create(user1, "qwertyuiopasdfghjklzx", True)

def test_invalid_is_public(setup_test_interface):
    user1, _ = setup_test_interface

    with pytest.raises(InputError):
        assert channels_create(user1, "channel_id", None)
    with pytest.raises(InputError):
        assert channels_create(user1, "channel_id", 0)
    with pytest.raises(InputError):
        assert channels_create(user1, "channel_id", "hi")

