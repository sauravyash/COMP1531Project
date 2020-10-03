############################################Channel Join Tests###################################
from channel import channel_join
from error import AccessError
from error import InputError
import pytest
# Success Join
def test_join_success():
    assert channel_join("VALID token", 1)  == {}

# Fail Join
def test_join_invalid_token():
    with pytest.raises(InputError) as e:
        channel_join("INVALID token", 1)

def test_join_invalid_chID():
    with pytest.raises(InputError) as e:
        channel_join("VALID token", 1)

def test_join_not_authorised():
    with pytest.raises(AccessError) as e:
        channel_join("VALID token", 1)
