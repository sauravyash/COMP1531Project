import auth
import channels
import other
import pytest
import random
import string
from channel import channel_invite
from channel import channel_messages
from error import InputError
from error import AccessError

# assume message id is an int
from message import message_send

def create_test_channel():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("good_email@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("good_email@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)

    channel_invite(result["token"], channel_id["channel_id"], result1["u_id"])

# Success Messages
# Sender Token must be valid
# Sender must be a member of the channel
# channel id must be valid
# message letters must be within 1000 characters
def test_valid_message_send():

    create_test_channel()
    assert message_send(result1["token"], channel_id["channel_id"], "Funky Monkey") == "valid_mID"

# Fail
# When the sender token is not valid
def test_invalid_message_token():

    create_test_channel()
    with pytest.raises(InputError):
        message_send("Invalid token", channel_id["channel_id"], "Funky Monkey")

# When the message sent to an invalid channel
def test_invalid_message_channel_id():

    create_test_channel()
    with pytest.raises(InputError):
        message_send(result1["token"], -1, "Funky Monkey")

# When the message exceeds 1000 character limit
def test_invalid_message_string_size_1000():

    create_test_channel()

    # Generate message exceeds 1000 on purpose
    # remove when implementation is complete
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(1005))
    
    with pytest.raises(InputError):
        message_send(result1["token"], channel_id["channel_id"], result_str)

# When the sender is not a member of the channel
def test_invalid_message_not_in_channel():

    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("good_email@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("good_email@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", False)

    # Not invited to the channel

    with pytest.raises(AccessError):
        message_send(result1["token"], channel_id["channel_id"], "Not in channel")
