#############################################Channel Addowner Tests###############################
from channel import channel_addowner
import pytest
from error import AccessError
from error import InputError
# Success Addowner
def test_addowner():
    assert (channel_addowner("VALID token", 1, 1)) == {}

# Fail Addowner
def test_addowner_invalid_token():
    with pytest.raises(InputError) as e:
        channel_addowner("INVALID token", 2, 2)

def test_addowner_invalid_chID():
    with pytest.raises(InputError) as e:
        channel_addowner("VALID token", 3, 3)

def test_addowner_invalid_uID():
    with pytest.raises(InputError) as e:
        channel_addowner("VALID token", 4, 4)

def test_addowner_not_authorised ():
    with pytest.raises(AccessError) as e:
        channel_addowner("VALID token", 5, 5)
