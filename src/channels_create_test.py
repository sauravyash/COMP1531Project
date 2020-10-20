import pytest
import other
import auth
from error import InputError
from error import AccessError
from channels import channels_create

### BLACKBOX TESTING ###

# Test for Valid Token
# - Token must be a string
# - Token cannot be empty
# - Token must be unique
#def test_channels_create_valid_token():
#    other.clear()
#    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', '#fname')
#    with pytest.raises(AccessError):
#        channels_create(0, "namee", True)
#    with pytest.raises(AccessError):
#        channels_create("", "namee", True)
#    with pytest.raises(AccessError):
#        channels_create(None, "namee", True)


# Test for Valid Name
# - Name must be a string
# - Name cannot be an empty String
# - Name cannot be longer than 20 chars
def test_channels_create_valid_name():
    other.clear()
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    result = auth.auth_login('validemail@gmail.com', 'validpassword')
    with pytest.raises(InputError):
        assert channels_create(result["token"], None, True)
    with pytest.raises(InputError):
        assert channels_create(result["token"], "", True)
    with pytest.raises(InputError):
        # 21 char length name
        assert channels_create(result["token"], "qwertyuiopasdfghjklzx", True)

# Test channel privacy
# - is_public is a boolean
def test_channels_create_is_public():
    other.clear()
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    result = auth.auth_login('validemail@gmail.com', 'validpassword')
    with pytest.raises(InputError):
        assert channels_create(result["token"], "nbamee", None)
    with pytest.raises(InputError):
        assert channels_create(result["token"], "dfdfdfs", 0)
    with pytest.raises(InputError):
        # 21 char length name
        assert channels_create(result["token"], "qweklzx", "hi")

# Test if passing with valid parameters
def test_channels_create_valid_all():
    other.clear()
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    result = auth.auth_login('validemail@gmail.com', 'validpassword')
    assert channels_create(result["token"], "channel_1", True)
    assert channels_create(result["token"], "channel_2", False)

# Test function output types
# - message_id is an int
#def test_channels_create_check_return_types():
#    assert isinstance(channels_create("tokebbb", "example_name", True), dict)
