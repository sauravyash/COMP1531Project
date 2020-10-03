#############################################Channel Removeowner Tests############################
from channel import channel_removeowner
from error import AccessError
from error import InputError
import pytest
# Success removeowner
def test_removeowner():
    assert channel_removeowner("VALID token", 6, 6) == {}

# Fail Removeowner
def test_removeowner_invalid_token():
    with pytest.raises(InputError) as e:
        channel_removeowner("INVALID token", 7, 7)
    
def test_removeowner_invalid_chID():
    with pytest.raises(InputError) as e:
        channel_removeowner("VALID token", 8, 8)

def test_removeowner_invalid_uID():
    with pytest.raises(InputError) as e:
        channel_removeowner("VALID token", 9, 9)

def test_removeowner_not_authorised():
    with pytest.raises(AccessError) as e:
        channel_removeowner("VALID token", 10, 10)