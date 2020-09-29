#######################################Channel Invite Tests#############################
from channel import channel_invite
import pytest
# Success Invite
def test_valid_invite():
    channel.channel_invite("VALID token", "VALID chID", "VALID uID")

# Fail Invite
def test_invite_invalid_token():
    with pytest.raises(InputError) as e:
        channel.channel_invite("INVALID token", "VALID chID", "VALID uID")

def test_invite_invalid_chID():
    with pytest.raises(InputError) as e:
        channel.channel_invite("VALID token", "INVALID chID", "VALID uID")

def test_invite_invalid_uID():
    with pytest.raises(InputError) as e:
        channel.channel_invite("VALID token", "VALID chID", "INVALID uID")

def test_invite_joined_uID():
    with pytest.raises(AccessError) as e:
        channel.channel_invite("VALID token", "VALID chID", "JOINED uID")