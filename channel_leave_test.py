###########################################Channel Leave Tests##################################
from channel import channel_leave
import pytest
# Success Leave
def test_leave_success():
    channel.channel_leave("VALID token", "VALID chID")

# Fail Leave
def test_leave_invalid_token():
    with pytest.raises(InputError) as e:
        channel.channel_leave("INVALID token", "VALID chID")

def test_leave_invalid_chID():
    with pytest.raises(InputError) as e:
        channel.channel_leave("VALID token", "INVALID chID")

def test_leave_user_not_channel():
    with pytest.raises(AccessError) as e:
        channel.channel_leave("VALID token", "VALID chID", "User Not Authorised")
  