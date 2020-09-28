#############################################Channel Removeowner Tests############################
from channel import channel_removeowner
import pytest
# Success removeowner
def test_removeowner():
    channel.channel_removeowner("VALID token", "VALID chID", "VALID uID")

# Fail Removeowner
def test_removeowner_invalid_token():
    with pytest.raises(InputError) as e:
        channel.channel_removeowner("INVALID token", "VALID chID", "VALID uID")
    
def test_removeowner_invalid_chID():
    with pytest.raises(InputError) as e:
        channel.channel_removeowner("VALID token", "INVALID chID", "VALID uID")

def test_removeowner_invalid_uID():
    with pytest.raises(InputError) as e:
        channel.channel_removeowner("VALID token", "VALID chID", "INVALID uID")

def test_removeowner_not_authorised():
    with pytest.raises(AcessError) as e:
        channel.channel_removeowner("VALID token", "VALID chID", "VALID uID", "User does not authorised", "Target is the owner")