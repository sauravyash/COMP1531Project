############################# Channel Details Tests ###########################
"""
Functions to test channel_details functionality
"""
import pytest

from error import AccessError
from error import InputError

from channel import channel_details
from channel import channel_invite

import auth
import channels
import other

from testing_fixtures.channel_test_fixtures import setup_test_interface

# ----- Success Details
def test_details_simple(setup_test_interface):
    user1, _, _, _ = setup_test_interface

    tok1 = user1["token"]

    # Create a channel with this user.
    channel_name = "test_channel"
    channel_id = channels.channels_create(tok1, channel_name, True)["channel_id"]

    # Check this user can access the channel's details.
    details = channel_details(tok1, channel_id)
    assert details["name"] == channel_name


def test_details_big(setup_test_interface):
    user1, user2, user3, _ = setup_test_interface

    tok1 = user1["token"]
    tok2 = user2["token"]
    uid2 = user2["u_id"]
    tok3 = user3["token"]

    # Create a channel with the first user.
    channel_name = "channel_x"
    channel_id = channels.channels_create(tok1, channel_name, True)["channel_id"]

    # Invite the second user to the channel.
    channel_invite(tok1, channel_id, uid2)

    # Check the first user can access the channel's details.
    assert channel_details(tok1, channel_id)["name"] == channel_name
    # Check the second user can also access these details.
    assert channel_details(tok2, channel_id)["name"] == channel_name

    # Check the third user doesn not have access to details.
    with pytest.raises(AccessError):
        channel_details(tok3, channel_id)


# ----- Fail Details
def test_not_member(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface

    user1["token"]
    tok2 = user2["token"]
    user2["u_id"]
    tok2 = user3["token"]
    channel_id = channel_dict["channel_id"]

    # Test that second user is not able to access channel details.
    with pytest.raises(AccessError):
        channel_details(tok2, channel_id)


def test_invalid_token(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface

    user1["token"]
    user2["token"]
    user2["u_id"]
    user3["token"]
    channel_id = channel_dict["channel_id"]

    # Check that Access Error is raised when invalid token is used.
    with pytest.raises(AccessError):
        channel_details("fake_token", channel_id)


def test_invalid_channel(setup_test_interface):
    user1, user2, user3, channel_dict = setup_test_interface

    tok1 = user1["token"]
    user2["token"]
    user2["u_id"]
    user3["token"]
    channel_dict["channel_id"]

    # Check that Input Error is raised when invalid channel is used.
    with pytest.raises(InputError):
        channel_details(tok1, -1)
