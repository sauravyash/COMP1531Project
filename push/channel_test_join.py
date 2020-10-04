############################################Channel Join Tests###################################
from channel import channel_join
import pytest
# Success Join
def test_join_success():
    channel.channel_join("VALID token", "VALID chID")

# Fail Join
def test_join_invalid_token():
    with pytest.raises(InputError) as e:
        channel.channel_join("INVALID token", "VALID chID")

def test_join_invalid_chID():
    with pytest.raises(InputError) as e:
        channel.channel_join("VALID token", "INVALID chID")

def test_join_not_authorised():
    with pytest.raises(AccessError) as e:
        channel.channel_join("VALID token", "VALID chID", "User Not AUthorised")
