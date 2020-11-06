############################ Channel Messages Test ############################
"""
Functions to test channel_messages functionality
"""
import pytest

from error import InputError
from error import AccessError

from channel import channel_messages
from channel import channel_invite

import auth
import channels
import message
import other
import data

from testing_fixtures.channel_test_fixtures import setup_test_interface

# ----- Success Messages
def test_messages_empty(setup_test_interface):
    user1, _, _, channel_dict = setup_test_interface

    tok1 = user1["token"]
    channel_id = channel_dict["channel_id"]

    # Check that user can access empty messages.
    result_messages = channel_messages(tok1, channel_id, 0)
    assert result_messages == {
        "messages": [],
        "start": 0,
        "end": -1,
    }


def test_messages_simple(setup_test_interface):
    user1, _, _, channel_dict = setup_test_interface

    tok1 = user1["token"]
    channel_id = channel_dict["channel_id"]

    # Send some messages.
    message.message_send(tok1, channel_id, "Hi")
    message.message_send(tok1, channel_id, "Hi Guys")
    message.message_send(tok1, channel_id, "Hi")
    message.message_send(tok1, channel_id, "Hello?")
    message.message_send(tok1, channel_id, "Hi All")
    message.message_send(tok1, channel_id, "Is anyone active?")
    message.message_send(tok1, channel_id, "...")
    message.message_send(tok1, channel_id, "Ummm...")
    message.message_send(tok1, channel_id, "Ok")
    message.message_send(tok1, channel_id, "Well")
    message.message_send(tok1, channel_id, "Seeya")
    message.message_send(tok1, channel_id, "*waves*")
    data.print_data()

    # Check that user can access these messages.
    result_messages = channel_messages(tok1, channel_id, 0)
    print(result_messages)
    assert len(result_messages["messages"]) == 12
    assert result_messages["messages"][11]["message"] == "Hi"
    assert result_messages["messages"][10]["message"] == "Hi Guys"
    assert result_messages["messages"][0]["message"] == "*waves*"


def test_channel_messages_pagination(setup_test_interface):
    user1, _, _, channel_dict = setup_test_interface

    tok1 = user1["token"]
    channel_id = channel_dict["channel_id"]

    test_msgs = [str(a) for a in range(200)]

    for x in test_msgs:
        # Send some messages.
        message.message_send(tok1, channel_id, x)

    for i in range(0, len(test_msgs), 50):
        result_messages = channel_messages(tok1, channel_id, i)

        assert result_messages["start"] == i

        for j in range(0, 50):
            assert (
                result_messages["messages"][j]["message"]
                == list(reversed(test_msgs))[i + j]
            )


# ----- Fail Messages
def test_not_member(setup_test_interface):
    _, user2, _, channel_dict = setup_test_interface

    tok2 = user2["token"]
    channel_id = channel_dict["channel_id"]

    # Test that second user is not a member of channel- cannot become owner.
    with pytest.raises(AccessError):
        channel_messages(tok2, channel_id, 0)


def test_invalid_channel(setup_test_interface):
    user1, _, _, _ = setup_test_interface

    tok1 = user1["token"]

    # Input error is raised when fake channel is used.
    with pytest.raises(InputError):
        channel_messages(tok1, -1, 0)


def test_invalid_start(setup_test_interface):
    user1, _, _, channel_dict = setup_test_interface

    tok1 = user1["token"]
    channel_id = channel_dict["channel_id"]

    # Input error is raised when start < 0.
    with pytest.raises(InputError):
        channel_messages(tok1, channel_id, -1)
    # Input error is raised when start > number of messages.
    with pytest.raises(InputError):
        channel_messages(tok1, channel_id, 30)


def test_invalid_token(setup_test_interface):
    _, _, _, channel_dict = setup_test_interface

    channel_id = channel_dict["channel_id"]

    # Access error is raised when a fake token is used.
    with pytest.raises(AccessError):
        channel_messages("fake_token", channel_id, 0)
