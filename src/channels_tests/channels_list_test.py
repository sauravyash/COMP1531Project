############################ Channels List Tests #############################
'''
Functions to test channels_list functionality
'''

import pytest

from error import AccessError

from channels import channels_list
from channels import channels_create

import channel

from testing_fixtures.channels_test_fixtures import setup_test_interface_lists
from testing_fixtures.channels_test_fixtures import setup_test_interface_create

# Test function output types
# - channel_id is an int
# - name is a string
def test_return_types(setup_test_interface_create):
    user1, _ = setup_test_interface_create
    channels_create(user1['token'], 'Hola_Seniora', True)

    for dictionary in channels_list(user1['token'])["channels"]:
        assert isinstance(dictionary['channel_id'], int)
        assert isinstance(dictionary['name'], str)

# Test empty list (no channels)
def test_channels_list_empty_list(setup_test_interface_create):
    user1, _ = setup_test_interface_create

    assert channels_list(user1["token"]) == {
        'channels': [] 
    }

# ----- Success List
def test_simple(setup_test_interface_lists):
    users, channels1, channels2, channels3 = setup_test_interface_lists
    created_channel_ids = [channels1, channels2, channels3]

    # For each user, test if they can see the channels they are a member of.
    for user in users:
        channel_list = channels_list(user['token'])
        returned_channel_ids = [ item['channel_id'] for item in channel_list['channels'] ]
        
        index = (user['u_id'] - 1)
        assert sorted(returned_channel_ids) == sorted(created_channel_ids[index])
        

def test_complex(setup_test_interface_lists):
    users, channels1, channels2, channels3 = setup_test_interface_lists

    # Separate users
    tok1 = users[0]['token']
    tok2 = users[1]['token']
    tok3 = users[2]['token']

    # Keep track of new members joining channels.
    channel.channel_join(tok1, channels2[0])
    channels1.append(channels2[0])
    channel.channel_join(tok2, channels1[0])
    channels2.append(channels1[0])

    # Test that new channels are listed correctly.
    channel_list1 = channels_list(tok1)
    channel_ids_1 = [item['channel_id'] for item in channel_list1['channels']]
    assert sorted(channel_ids_1) == sorted(channels1)

    channel_list2 = channels_list(tok2)
    channel_ids_2 = [item['channel_id'] for item in channel_list2['channels']]
    assert sorted(channel_ids_2) == sorted(channels2)

    channel_list3 = channels_list(tok3)
    channel_ids_3 = [item['channel_id'] for item in channel_list3['channels']]
    assert sorted(channel_ids_3) == sorted(channels3)

# ----- Fail List
def test_invalid_token(setup_test_interface_create):
    
    user1, _ = setup_test_interface_create
    
    # Create a channel with first user.
    channels_create(user1['token'], 'channel_1', True)
    
    # Check that Access Error is raised when invalid token is used.
    with pytest.raises(AccessError):
        channels_list('fake_token')

