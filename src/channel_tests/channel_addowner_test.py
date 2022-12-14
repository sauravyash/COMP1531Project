########################### Channel Addowner Tests ############################
"""
Functions to test channel_addowner functionality
"""
import pytest

from error import AccessError
from error import InputError

from channel import channel_addowner
from channel import channel_invite
from channel import channel_details
from channel import channel_join

import auth
import channels
import other

from testing_fixtures.channel_test_fixtures import setup_test_interface

# ----- Success Addowner
def test_addowner_simple(setup_test_interface):
    user1, user2, _, channel_dict = setup_test_interface

    tok1 = user1["token"]
    uid2 = user2["u_id"]
    channel_id = channel_dict["channel_id"]

    # Invite the second user to the channel.
    channel_invite(tok1, channel_id, uid2)

    # Check that the second user successfully becomes an owner in the channel.
    assert len(channel_details(tok1, channel_id)["owner_members"]) == 1
    assert channel_addowner(tok1, channel_id, uid2) == {}
    assert len(channel_details(tok1, channel_id)["owner_members"]) == 2


def test_flockr_owner(setup_test_interface):
    user1, user2, user3, _ = setup_test_interface

    tok1 = user1["token"]
    uid2 = user2["u_id"]
    tok3 = user3["token"]

    # Overwrite channel_id with the second user for testing different admin configurations
    channel_id = channels.channels_create(tok3, "channel_2", True)["channel_id"]

    # Invite the second user to the channel.
    channel_join(tok1, channel_id)
    channel_invite(tok1, channel_id, uid2)

    # Check that the flockr owner can still make other members owners.
    assert len(channel_details(tok3, channel_id)["owner_members"]) == 1
    assert channel_addowner(tok3, channel_id, uid2) == {}
    assert len(channel_details(tok1, channel_id)["owner_members"]) == 2


# ----- Fail Addowner
def test_not_member(setup_test_interface):
    user1, user2, _, channel_dict = setup_test_interface

    tok1 = user1["token"]
    uid2 = user2["u_id"]
    channel_id = channel_dict["channel_id"]
    # Test that second user is not a member of channel- cannot become owner.
    with pytest.raises(InputError):
        channel_addowner(tok1, channel_id, uid2)


def test_invalid_token(setup_test_interface):
    user1, user2, _, channel_dict = setup_test_interface

    tok1 = user1["token"]
    uid2 = user2["u_id"]
    channel_id = channel_dict["channel_id"]

    # Invite the second user to the channel.
    channel_invite(tok1, channel_id, uid2)

    # Check that Access Error is raised when invalid token is used.
    with pytest.raises(AccessError):
        channel_addowner("fake_token", channel_id, uid2)


def test_invalid_user_id(setup_test_interface):
    user1, user2, _, channel_dict = setup_test_interface

    tok1 = user1["token"]
    uid2 = user2["u_id"]
    channel_id = channel_dict["channel_id"]

    # Invite the second user to the channel.
    channel_invite(tok1, channel_id, uid2)

    # Check that Access Error is raised when invalid token is used.
    with pytest.raises(InputError):
        channel_addowner("fake_token", channel_id, -1)


def test_invalid_channel(setup_test_interface):
    user1, user2, _, channel_dict = setup_test_interface

    tok1 = user1["token"]
    uid2 = user2["u_id"]
    channel_id = channel_dict["channel_id"]

    # Invite the second user to the channel.
    channel_invite(tok1, channel_id, uid2)

    # Check that Input Error is raised when invalid channel is used.
    with pytest.raises(InputError):
        channel_addowner(tok1, -1, uid2)


def test_not_authorized(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1["token"]
    uid2 = user2["u_id"]
    tok3 = user3["token"]
    uid3 = user3["u_id"]
    channel_id = channel_dict["channel_id"]

    # Invite the second & third users to the channel.
    channel_invite(tok1, channel_id, uid2)
    channel_invite(tok1, channel_id, uid3)

    # Second member tries to add third member as owner- raise Access Error.
    with pytest.raises(AccessError):
        channel_addowner(tok3, channel_id, uid2)


def test_already_owner(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1["token"]
    uid2 = user2["u_id"]
    tok3 = user3["token"]
    uid3 = user3["u_id"]

    channel_id = channel_dict["channel_id"]

    # Invite the second & third users to the channel.
    channel_invite(tok1, channel_id, uid3)
    channel_invite(tok3, channel_id, uid2)

    # Make second user an owner of the channel.
    channel_addowner(tok1, channel_id, uid2)

    # Second user is already an owner- raise Input Error.
    with pytest.raises(InputError):
        channel_addowner(tok1, channel_id, uid2)
