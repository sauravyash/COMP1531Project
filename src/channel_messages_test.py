############################ Channel Messages Test ############################
'''
Functions to test channel_messages functionality
'''
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


# ----- Success Messages
def test_messages_empty():

    other.clear()

    # Register and login one user.
    auth.auth_register('validemail@gmail.com', 'password123', 'fname', 'lname')
    result = auth.auth_login('validemail@gmail.com', 'password123')

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel_invite(result1["token"], channel_id["channel_id"], result1["u_id"])
    message_send(result1["token"], channel_id["channel_id"], "Hello There")
    check = channel_messages(result1["token"], channel_id["channel_id"], 0)
    assert check["end"] == -1
    assert check["start"] == 0
    assert check["messages"][0]["u_id"] == 2
    assert check["messages"][0]["message"] == "Hello There"

# Fail
def test_invalid_channel_messages_id():
    ''' Invalid Channel ID'''
    other.clear()

    # Register and login one user.
    auth.auth_register('validemail@gmail.com', 'password123', 'fname', 'lname')
    result = auth.auth_login('validemail@gmail.com', 'password123')

    # Create a channel with the first user.
    channel_id = channels.channels_create(result['token'], 'channel_1', True)

    # Send some messages.
    message.message_send(result['token'], channel_id['channel_id'], 'Hi')
    message.message_send(result['token'], channel_id['channel_id'], 'Hi Guys')
    message.message_send(result['token'], channel_id['channel_id'], 'Hi')
    message.message_send(result['token'], channel_id['channel_id'], 'Hello?')
    message.message_send(result['token'], channel_id['channel_id'], 'Hi All')
    message.message_send(result['token'], channel_id['channel_id'], 'Is anyone active?')
    message.message_send(result['token'], channel_id['channel_id'], '...')
    message.message_send(result['token'], channel_id['channel_id'], 'Ummm...')
    message.message_send(result['token'], channel_id['channel_id'], 'Ok')
    message.message_send(result['token'], channel_id['channel_id'], 'Well')
    message.message_send(result['token'], channel_id['channel_id'], 'Seeya')
    message.message_send(result['token'], channel_id['channel_id'], '*waves*')
    data.print_data()

    # Check that user can access these messages.
    result_messages = channel_messages(result['token'], channel_id['channel_id'], 0)
    print(result_messages)
    assert len(result_messages['messages']) == 12
    assert result_messages['messages'][11]['message'] == 'Hi'
    assert result_messages['messages'][10]['message'] == 'Hi Guys'
    assert result_messages['messages'][0]['message'] == '*waves*'

def test_channel_messages_pagination():
    other.clear()

    # Register and login one user.
    auth.auth_register('validemail@gmail.com', 'password123', 'fname', 'lname')
    result = auth.auth_login('validemail@gmail.com', 'password123')

    # Create a channel with the first user.
    channel_id = channels.channels_create(result['token'], 'channel_1', True)

    test_msgs = [str(a) for a in range(200)]

    for x in test_msgs:
        # Send some messages.
        message.message_send(result['token'], channel_id['channel_id'], x)

    for i in range(0, len(test_msgs), 50):
        result_messages = channel_messages(result['token'], channel_id['channel_id'], i)

        assert result_messages['start'] == i

        for j in range(0, 50):
            assert result_messages['messages'][j]['message'] == list(reversed(test_msgs))[i + j]

# ----- Fail Messages
def test_not_member():

    other.clear()

    # Register and login two users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    result1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    result2 = auth.auth_login('validemail2@gmail.com', 'password123')

    # Create a channel with the first user.
    channel_id = channels.channels_create(result1['token'], 'channel_1', True)

    # Test that second user is not a member of channel- cannot become owner.
    with pytest.raises(AccessError):
        channel_messages(result2['token'], channel_id['channel_id'], 0)

def test_invalid_channel():

    other.clear()

    # Register and login a user.
    auth.auth_register('validemail@gmail.com', 'password123', 'fname', 'lname')
    result = auth.auth_login('validemail@gmail.com', 'password123')

    # Create a channel with this user.
    channels.channels_create(result['token'], 'channel_1', True)

    # Input error is raised when fake channel is used.
    with pytest.raises(InputError):
        channel_messages(result['token'], -1, 0)

def test_invalid_start():

    other.clear()

    # Register and login a user.
    auth.auth_register('validemail@gmail.com', 'password123', 'fname', 'lname')
    result = auth.auth_login('validemail@gmail.com', 'password123')

    # Create a channel with this user.
    channel_id = channels.channels_create(result['token'], 'channel_1', True)

    # Input error is raised when start < 0.
    with pytest.raises(InputError):
        channel_messages(result['token'], channel_id['channel_id'], -1)
    # Input error is raised when start > number of messages.
    with pytest.raises(InputError):
        channel_messages(result['token'], channel_id['channel_id'], 30)

def test_invalid_token():

def test_invalid_channel_messages_authorised():
    ''' not a member of the channel'''
    other.clear()

    # Register and login a user.
    auth.auth_register('validemail@gmail.com', 'password123', 'fname', 'lname')
    result = auth.auth_login('validemail@gmail.com', 'password123')

    # Create a channel with first user.
    channel_id = channels.channels_create(result['token'], 'channel_1', True)

    # Access error is raised when a fake token is used.
    with pytest.raises(AccessError):
        channel_messages('fake_token', channel_id['channel_id'], 0)
