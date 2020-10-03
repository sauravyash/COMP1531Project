import pytest

from channels import channels_create

### BLACKBOX TESTING ###

# Test for Valid Token
# - Token must be a string
# - Token cannot be empty
# - Token must be unique
def test_channels_create_valid_token():
    with pytest.raises(InputError) as e:
        channels_create(0, "namee", True)
    with pytest.raises(InputError) as e:
        channels_create("", "namee", True)
    with pytest.raises(InputError) as e:
        channels_create(None, "namee", True)


# Test for Valid Name
# - Name must be a string
# - Name cannot be an empty String
# - Name cannot be longer than 20 chars
def test_channels_create_valid_name(): 
    with pytest.raises(InputError) as e:
        channels_create("123421", None, True)
    with pytest.raises(InputError) as e:
        channels_create("234234", "", True)
    with pytest.raises(InputError) as e:
        # 21 char length name
        channels_create("233422", "qwertyuiopasdfghjklzx", True)

# Test channel privacy
# - is_public is a boolean
def test_channels_create_is_public():
    with pytest.raises(InputError) as e:
        channels_create("123421", "nbamee", None)
    with pytest.raises(InputError) as e:
        channels_create("234234", "dfdfdfs", 0)
    with pytest.raises(InputError) as e:
        # 21 char length name
        channels_create("233422", "qweklzx", "hi")

# Test function output types
# - message_id is an int
def test_channels_create_check_return_types():
    assert isinstance(channels_create("", "", True), dict)





