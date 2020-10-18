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
from message import message_edit


def create_test_channel():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("good_email@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("good_email@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel_invite(result["token"], channel_id["channel_id"], result1["u_id"])

# Success Messages
# Valid sender token
# Valid message ID
# Edited message within 1000 charactre limit
# Edit authorized by owner or sender
def test_valid_message_edit():

    create_test_channel()
    meesage1 = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    assert message_edit(result1["token"], message1, "Monkey Funky") == {}


def test_authorized_edit():
 
    create_test_channel()
    meesage1 = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    assert message_edit(result["token"], message1, "Monkey Funky") == {}    


#Fail
# Invalid sender/owner token
def test_invalid_token():

    create_test_channel()
    message1 = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    with pytest raises(InputError):
        message_edit("Invalid token", message1, "Monkey Funky") == {}

# Invalid message ID
def test_invalid_message_id():

    create_test_channel()
    message1 = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    with pytest raises(InputError):
        message_edit(result1["token"], -1, "Monkey Funky") == {}

# Message edit size over 1000
def test_invalid_message_edit_exceeds_size_limit():

    create_test_channel()
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(1005))
    message1 = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    with pytest raises(InputError):
        message_edit(result1["token"], message1, result_str) == {}    

# Edit authorization from not a sender
def test_invalid_message_edit_not_sender():

    create_test_channel()

    auth.auth_register("awsome_email@gmail.com", "password123", "fname2", "lname2")
    result2 = auth.auth_login("awsome_email@gmail.com", "password123")
    channel_invite(result["token"], channel_id["channel_id"], result2["u_id"])

    message1 = message_send(result1["token"], channel_id["channel_id"], "Funky Monkey")
    with pytest raises(AccessError):
        message_edit(result2["token"], message1, "Monkey Funky") == {}    

# Member trying to edit message from owner
def test_invalid_message_edit_not_authorized():
    create_test_channel()

    auth.auth_register("awsome_email@gmail.com", "password123", "fname2", "lname2")
    result2 = auth.auth_login("awsome_email@gmail.com", "password123")
    channel_invite(result["token"], channel_id["channel_id"], result2["u_id"])

    message1 = message_send(result["token"], channel_id["channel_id"], "Funky Monkey")
    with pytest raises(AccessError):
        message_edit(result2["token"], message1, "Monkey Funky") == {}      

