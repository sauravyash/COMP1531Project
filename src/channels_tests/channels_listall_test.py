import pytest

from channels import channels_listall

### BLACKBOX TESTING ###

# Test empty list (no channels)
def test_channels_listall_empty_list():
    assert channels_listall("") == {}

# Test list of many channels


# Test function output types
# - message_id is an int
# - name is a string
def test_channels_create_check_return_types():
    assert isinstance(channels_listall(""), dict)

