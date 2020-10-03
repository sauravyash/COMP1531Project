#######################################Channel Invite Tests#############################
from channel import channel_invite
from error import InputError
from error import AccessError
import pytest

# Success Invite
def test_valid_invite():
   assert channel_invite("VALID token5", 1, 5) == {}

# Fail Invite
def test_invite_invalid_token():
    with pytest.raises(InputError) as e:
        channel_invite("INVALID token", 1, 1)

def test_invite_invalid_chID():
    with pytest.raises(InputError) as e:
        channel_invite("VALID token", "INVALID chID", 1)

def test_invite_invalid_uID():
    with pytest.raises(InputError) as e:
        channel_invite("VALID token", "1", "INVALID uID")

def test_invite_joined_uID():
    with pytest.raises(AccessError) as e:
        channel_invite("VALID token", 1, 1)
