########################### Channels Listall Tests ############################
'''
Functions to test channels_listall functionality
'''

import pytest

from error import AccessError

from channels import channels_create
from channels import channels_listall

from testing_fixtures.channels_test_fixtures import setup_test_interface_lists
from testing_fixtures.channels_test_fixtures import setup_test_interface_create

# Test function output types
# - channel_id is an int
# - name is a string
def test_return_types(setup_test_interface_create):
    user1, _ = setup_test_interface_create
    channels_create(user1['token'], 'channel_1', True)

    for dictionary in channels_listall(user1['token'])['channels']:
        assert isinstance(dictionary['channel_id'], int)
        assert isinstance(dictionary['name'], str)

# ----- Success Listall
def test_simple(setup_test_interface_lists):
    users, channels1, channels2, channels3 = setup_test_interface_lists
    created_channel_ids = channels1 + channels2 + channels3

    # For each user, test if they can see all channels created.
    for user in users:
        channel_list = channels_listall(user['token'])
        returned_channel_ids = [ item['channel_id'] for item in channel_list['channels'] ]

        assert sorted(returned_channel_ids) == sorted(created_channel_ids)

# ----- Fail Listall
def test_invalid_token(setup_test_interface_create):
    user1, _ = setup_test_interface_create
    # Create a channel with first user.
    channels_create(user1['token'], 'channel_1', True)
    
    # Check that Access Error is raised when invalid token is used.
    with pytest.raises(AccessError):
        channels_listall('fake_token')

