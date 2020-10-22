import pytest

import channels
import auth
import data

from other import clear
from error import AccessError

### BLACKBOX TESTING ###

# Test function output types
# - channel_id is an int
# - name is a string
def test_channels_listall_check_return_types():
    # Clear existing data...
    clear()

    # Set up user and create channel...
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Tara', 'Andresson')
    token_dict = auth.auth_login('validemail@gmail.com', '123abc!@#')
    channels.channels_create(token_dict['token'], 'Hola_Seniora', True)

    for dictionary in channels.channels_listall(token_dict['token']):
        assert isinstance(dictionary['channel_id'], int)
        assert isinstance(dictionary['name'], str)

# ----- Success Listall
def test_channels_listall_public_only():
    # Clear existing data...
    clear()

    # Set up user and create a channel...
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Tara', 'Andresson')
    token_dict = auth.auth_login('validemail@gmail.com', '123abc!@#')
    channel_1 = channels.channels_create(token_dict['token'], 'Hola_Seniora', True)
    channel_2 = channels.channels_create(token_dict['token'], 'ILoveIcecream', True)

    # (Only public)
    assert channels.channels_listall(token_dict['token']) == [
    {'channel_id': channel_1['channel_id'], 'name': 'Hola_Seniora'},
    {'channel_id': channel_2['channel_id'], 'name': 'ILoveIcecream'}]


def test_channels_listall_public_private():
    # Clear existing data...
    clear()

    # Set up 2 users and create multiple channels...
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Tara', 'Andresson')
    token_1 = auth.auth_login('validemail@gmail.com', '123abc!@#')

    auth.auth_register('validemail2@gmail.com', '1234abc!@#', 'Jess', 'Apples')
    token_2 = auth.auth_login('validemail2@gmail.com', '1234abc!@#')

    channel_1 = channels.channels_create(token_1['token'], 'Hola_Seniora', True)
    channel_2 = channels.channels_create(token_2['token'], 'ILoveIcecream', True)
    channel_3 = channels.channels_create(token_1['token'], 'ImAnEngineer', False)
    channel_4 = channels.channels_create(token_2['token'], 'HugsOnly', False)

    # (Public & private)
    assert channels.channels_listall(token_1['token']) == [
    {'channel_id': channel_1['channel_id'], 'name': 'Hola_Seniora'},
    {'channel_id': channel_2['channel_id'], 'name': 'ILoveIcecream'},
    {'channel_id': channel_3['channel_id'], 'name': 'ImAnEngineer'},
    {'channel_id': channel_4['channel_id'], 'name': 'HugsOnly'}]

# ----- Fail Listall
def test_invalid_token():
    
    clear()
    
    # Register and login a user.
    auth.auth_register('validemail@gmail.com', 'password123', 'fname', 'lname')
    result = auth.auth_login('validemail@gmail.com', 'password123')
    
    # Create a channel with first user.
    channel_id = channels.channels_create(result['token'], 'channel_1', True)
    
    # Check that Access Error is raised when invalid token is used.
    with pytest.raises(AccessError):
        channels.channels_listall('fake_token')
