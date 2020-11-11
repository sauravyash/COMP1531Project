############################ Channels Create Tests #############################
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

from testing_fixtures.channels_test_fixtures import setup_test_interface_create

# ----- Success Create
def test_simple(setup_test_interface_create):
    user1, _ = setup_test_interface_create
    tok1 = user1['token']

    channel_1 = channels_create(tok1, "channel_1", True)['channel_id']
    assert len(channel.channel_details(tok1, channel_1)['owner_members']) == 1
    assert len(channel.channel_details(tok1, channel_1)['all_members']) == 1

    channel_2 = channels_create(tok1, "channel_2", False)['channel_id']
    assert len(channel.channel_details(tok1, channel_2)['owner_members']) == 1
    assert len(channel.channel_details(tok1, channel_2)['all_members']) == 1

def test_multiple_users(setup_test_interface_create):
    user1, user2 = setup_test_interface_create
    tok1 = user1['token']
    tok2 = user2['token']

    channel_1 = channels_create(tok1, "channel_1", True)['channel_id']
    assert len(channel.channel_details(tok1, channel_1)['owner_members']) == 1
    assert len(channel.channel_details(tok1, channel_1)['all_members']) == 1

    channel_2 = channels_create(tok2, "channel_2", False)['channel_id']
    assert len(channel.channel_details(tok2, channel_2)['owner_members']) == 1
    assert len(channel.channel_details(tok2, channel_2)['all_members']) == 1

# ----- Fail Create
def test_invalid_token(setup_test_interface_create):
    setup_test_interface_create

    with pytest.raises(AccessError):
        channels_create(0, "channel_id", True)
    with pytest.raises(AccessError):
        channels_create("", "channel_id", True)
    with pytest.raises(AccessError):
        channels_create(None, "channel_id", True)

def test_invalid_channel_name(setup_test_interface_create):
    user1, _ = setup_test_interface_create
    tok1 = user1['token']
    
    with pytest.raises(InputError):
        assert channels_create(tok1, None, True)
    with pytest.raises(InputError):
        assert channels_create(tok1, "", True)
    with pytest.raises(InputError):
        # 21 char length name
        assert channels_create(tok1, "qwertyuiopasdfghjklzx", True)

def test_invalid_is_public(setup_test_interface_create):
    user1, _ = setup_test_interface_create
    tok1 = user1['token']

    with pytest.raises(InputError):
        assert channels_create(tok1, "channel_id", None)
    with pytest.raises(InputError):
        assert channels_create(tok1, "channel_id", 0)
    with pytest.raises(InputError):
        assert channels_create(tok1, "channel_id", "hi")

