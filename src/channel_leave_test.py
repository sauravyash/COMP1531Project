###########################################Channel Leave Tests##################################
from channel_leave import channel_leave
from error import InputError
from error import AccessError
import pytest
# Success Leave
def test_leave_success():
    channel_leave("VALID token", 1)

# Fail Leave
def test_leave_invalid_token():
    with pytest.raises(InputError) as e:
        channel_leave("INVALID token", 1)

def test_leave_invalid_chID():
    with pytest.raises(InputError) as e:
        channel_leave("VALID token", "INVALID chID")

def test_leave_user_not_channel():
    with pytest.raises(AccessError) as e:
        channel_leave("VALID token5", 1)