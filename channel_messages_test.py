from channel import channel_messages
import pytest
# Success Channel Messages Tests
def test_valid_message():
    channel.channel_messages("VALID token","VALID chID", "start")

# Fail Showing messages
def test_message_invalid_token():
    with pytest.raises(InputError) as e:
        channel.channel_messages("INVALID token", "VALID chID", "start")

def test_message_invalid_chID():
    with pytest.raises(InputError) as e:
        channel.channel_messages("VALID token", "INVALID chID", "start")

def test_message_invalid_start():
    with pytest.raises(InputError) as e:
        channel.channel_messages("VALID token", "VALID chID", "INVALID start")

def test_message_not_authorised():
    with pytest.raises(AccessError) as e:
        channel.channel_messages("VALID token", "VALID chID", "start", "User Not Authorised")
