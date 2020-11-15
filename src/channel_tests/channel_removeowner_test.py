############################ Channel Removeowner Tests ########################
"""
Functions to test channel_removeowner functionality
"""
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

from testing_fixtures.channel_test_fixtures import setup_test_interface

# ----- Success Removeowner
def test_remove_owner_simple(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1["token"]
    user2["token"]
    uid2 = user2["u_id"]
    user3["token"]
    channel_id = channel_dict["channel_id"]

    # Invite the second user to the channel.
    channel_invite(tok1, channel_id, uid2)

    # Add the second user as an owner.
    assert channel_addowner(tok1, channel_id, uid2) == {}

    # Check that second user's owner status is removed.
    assert len(channel_details(tok1, channel_id)["owner_members"]) == 2
    assert channel_removeowner(tok1, channel_id, uid2) == {}
    assert len(channel_details(tok1, channel_id)["owner_members"]) == 1


def test_flockr_owner(setup_test_interface):
    user1, user2, user3, _ = setup_test_interface

    user1["token"]
    uid1 = user1["u_id"]
    tok2 = user2["token"]
    uid2 = user2["u_id"]
    tok3 = user3["token"]
    uid3 = user3["u_id"]
    channel_id = channels.channels_create(tok2, "cl_9", False)["channel_id"]

    # Invite the second user to the channel.
    channel_invite(tok2, channel_id, uid1)
    channel_invite(tok2, channel_id, uid3)

    # Second user (owner of channel) adds third user as a channel owner.
    assert channel_addowner(tok2, channel_id, uid3) == {}

    # Check that flockr owner can also remove a channel owner.
    assert len(channel_details(tok2, channel_id)["owner_members"]) == 2
    assert channel_removeowner(tok3, channel_id, uid2) == {}
    assert len(channel_details(tok3, channel_id)["owner_members"]) == 1


# ----- Fail Removeowner
def test_not_member(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1["token"]
    user2["token"]
    uid2 = user2["u_id"]
    user3["token"]
    channel_id = channel_dict["channel_id"]

    # Test that second user is not a member of channel- cannot become owner.
    with pytest.raises(InputError):
        channel_removeowner(tok1, channel_id, uid2)


def test_invalid_token(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1["token"]
    user2["token"]
    uid2 = user2["u_id"]
    user3["token"]
    channel_id = channel_dict["channel_id"]

    # Invite the second user to the channel.
    channel_invite(tok1, channel_id, uid2)

    # Check that Access Error is raised when invalid token is used.
    with pytest.raises(AccessError):
        channel_removeowner("fake_token", channel_id, uid2)


def test_invalid_user_id(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1["token"]
    user2["token"]
    uid2 = user2["u_id"]
    user3["token"]
    channel_id = channel_dict["channel_id"]

    # Invite the second user to the channel.
    channel_invite(tok1, channel_id, uid2)

    # Check that Access Error is raised when invalid token is used.
    with pytest.raises(InputError):
        channel_removeowner("fake_token", channel_id, -1)


def test_invalid_channel(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1["token"]
    user2["token"]
    uid2 = user2["u_id"]
    user3["token"]
    channel_id = channel_dict["channel_id"]

    # Invite the second user to the channel.
    channel_invite(tok1, channel_id, uid2)

    # Check that Input Error is raised when invalid channel is used.
    with pytest.raises(InputError):
        channel_removeowner(tok1, -1, uid2)


def test_not_authorized(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1["token"]
    tok2 = user2["token"]
    uid2 = user2["u_id"]
    user3["token"]
    uid3 = user3["u_id"]
    uid1 = user1["u_id"]
    channel_id = channel_dict["channel_id"]

    # Invite the second & third users to the channel.
    channel_invite(tok1, channel_id, uid2)
    channel_invite(tok2, channel_id, uid3)

    # Second member (not owner) tries to remove first member (owner)- raise Access Error.
    with pytest.raises(AccessError):
        channel_removeowner(tok2, channel_id, uid1)


def test_not_owner(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1["token"]
    tok2 = user2["token"]
    uid2 = user2["u_id"]
    user3["token"]
    uid3 = user3["u_id"]
    channel_id = channel_dict["channel_id"]

    # Invite the second & third users to the channel.
    channel_invite(tok1, channel_id, uid2)
    channel_invite(tok2, channel_id, uid3)

    # First member (owner) tries to remove second member (not owner)- raise Input Error.
    with pytest.raises(InputError):
        channel_removeowner(tok1, channel_id, uid2)
