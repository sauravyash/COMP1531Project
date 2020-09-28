###########################################Channel Deatil Tests################################
from channel import channel_detail
import pytest
# Success Showing Detail
def test_valid_detail():
    channel.channel_detail("VALID token", "VALID chID")

# Fail Showing Detail
def test_detail_invalid_token():
    with pytest.raises(InputError) as e:
        channel.channel_detail("INVALID token", "VALID chID")

def test_detail_invalid_chID():
    with pytest.raises(InputError) as e:
        channel.channel_detail("VALID token", "INVALID chID")

def test_detail_not_authorised():
    with pytest.raises(AccessError) as e:
        channel.channel_detail("VALID chID", "User Not Authorised")