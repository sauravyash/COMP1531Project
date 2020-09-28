#############################################Channel Addowner Tests###############################
from channel import channel_addowner
import pytest
# Success Addowner
def test_addowner():
    channel.channel_addowner("VALID token", "VALID chID", "VALID uID")

# Fail Addowner
def test_addowner_invalid_token():
    with pytest.raises(InputError) as e:
        channel.channel_addowner("INVALID token", "VALID chID", "VALID uID")

def test_addowner_invalid_chID():
    with pytest.raises(InputError) as e:
        channel.channel_addowner("VALID token", "INVALID chID", "VALID uID")

def test_addowner_invalid_uID():
    with pytest.raises(InputError) as e:
        channel.channel_addowner("VALID token", "VALID chID", "INVALID uID")

def test_addowner_not_authorised ():
    with pytest.raises(AcessError) as e:
        channel.channel_addowner("VALID token", "VALID chID", "VALID chID", "User is not a member or User is already an owner")
