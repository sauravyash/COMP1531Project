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
from message import message_remove


def create_test_channel():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("newvalidemail@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("newgood_email@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel_invite(result["token"], channel_id["channel_id"], result1["u_id"]) 



# Success Messages Remove
# Remove must be from owner of the channel or sender of the message
# Owner/Sender token must be valid
# Channel id must be valid
def test_valid_message_remove():

    create_test_channel()
    message1 = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    assert message_remove(result1["token"], message1) == {}

def test_valid_message_remove_authorized():

    create_test_channel
    message1 = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    assert message_remove(result["token"], message1) == {}

# Fail
# Invalid Sender token
def test_invalid_message_token():

    create_test_channel()
    message1 = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    with pytest.raises(InputError):
        message_remove("Invalid token", message1)

# Invalid message ID
def test_invalid_message_id():

    create_test_channel()
    message1 = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    with pytest.raises(InputError):
        message_remove(result1["token"], -1)

################################
# When the message is already removed
def test_invalid_message_removed():

    create_test_channel()
    message1 = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    message_remove(result1["token"], message1)

    with pytest.raises(InputError):
        message_remove(result1["token"], message1)

# When the remove is authorized from a member that is not send or owner
def test_invalid_message_remove_not_sender():
    create_test_channel()

    auth.auth_register("awsome_email2@gmail.com", "password123", "fname2", "lname2")
    result2 = auth.auth_login("awsome_email2@gmail.com", "password123")

    channel_invite(result2["token"], channel_id["channel_id"], result2["u_id"])

    message1 = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    with pytest.raises(AccessError):
        message_remove(result2["token"], message1)

# When the remove is authorized from a member that is not send or owner
def test_invalid_message_remove_not_authorized():
    create_test_channel()

    auth.auth_register("awsome_email2@gmail.com", "password123", "fname2", "lname2")
    result2 = auth.auth_login("awsome_email2@gmail.com", "password123")

    channel_invite(result2["token"], channel_id["channel_id"], result2["u_id"])

    message1 = message_send(result["token"], channel_id["channel_id"], "Funky Monkey")
    with pytest.raises(AccessError):
        message_remove(result2["token"], message1)