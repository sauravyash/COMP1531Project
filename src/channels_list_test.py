import pytest

from error import AccessError

from channels import channels_list
from channels import channels_create
import channels
import channel
import data
import auth
import other

### BLACKBOX TESTING ###

# Test function output types
# - channel_id is an int
# - name is a string
def test_channels_list_check_return_types():
    # Clear existing data...
    other.clear()

    # Set up user and create channel...
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Tara', 'Andresson')
    token_dict = auth.auth_login('validemail@gmail.com', '123abc!@#')
    channels_create(token_dict['token'], 'Hola_Seniora', True)

    for dictionary in channels_list(token_dict['token']):
        assert isinstance(dictionary['channel_id'], int)
        assert isinstance(dictionary['name'], str)

# Test empty list (no channels)
def test_channels_list_empty_list():
    # Clear existing data...
    other.clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Tara', 'Andresson')
    login_info = auth.auth_login('validemail@gmail.com', '123abc!@#')

    assert channels.channels_list(login_info["token"]) == []

# Test list of many channels (for when we implement other functions)
# ----- Success List
def test_channels_list_public_only():
    # Clear existing data.
    other.clear()

    # Set up user and create a channel.
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Tara', 'Andresson')
    token_dict = auth.auth_login('validemail@gmail.com', '123abc!@#')
    channel_1 = channels_create(token_dict['token'], 'Hola_Seniora', True)
    channel_2 = channels_create(token_dict['token'], 'ILoveIcecream', True)

    # (Only public)
    assert channels_list(token_dict['token']) == [
    {'channel_id': channel_1['channel_id'], 'name': 'Hola_Seniora'},
    {'channel_id': channel_2['channel_id'], 'name': 'ILoveIcecream'}]

def test_channels_list_public_private():
    # Clear data
    other.clear()

    # Set up 3 users and create multiple channels...
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Tara', 'Andresson')
    auth.auth_login('validemail@gmail.com', '123abc!@#')

    auth.auth_register('validemail1@gmail.com', '123abc!@#', 'Genine', 'Buggsies')
    token_1 = auth.auth_login('validemail1@gmail.com', '123abc!@#')

    auth.auth_register('validemail2@gmail.com', '1234abc!@#', 'Jess', 'Apples')
    token_2 = auth.auth_login('validemail2@gmail.com', '1234abc!@#')

    channel_1 = channels_create(token_1['token'], 'Hola_Seniora', True)
    channel_2 = channels_create(token_2['token'], 'ILoveIcecream', True)
    channel_3 = channels_create(token_1['token'], 'ImAnEngineer', False)
    channel_4 = channels_create(token_2['token'], 'HugsOnly', False)
    
    channel.channel_join(token_1['token'], channel_2['channel_id'])
    channel.channel_join(token_2['token'], channel_1['channel_id'])
    channel.channel_addowner(token_2['token'], channel_2['channel_id'], token_1['u_id'])

    # (Public & private)
    assert channels_list(token_1['token']) == [
    {'channel_id': channel_1['channel_id'], 'name': 'Hola_Seniora'},
    {'channel_id': channel_2['channel_id'], 'name': 'ILoveIcecream'},
    {'channel_id': channel_3['channel_id'], 'name': 'ImAnEngineer'},]

    assert channels_list(token_2['token']) == [
    {'channel_id': channel_1['channel_id'], 'name': 'Hola_Seniora'},
    {'channel_id': channel_2['channel_id'], 'name': 'ILoveIcecream'},
    {'channel_id': channel_4['channel_id'], 'name': 'HugsOnly'},]


def test_channels_list_owner_priv():
    # Clear data
    other.clear()

    # Set up 3 users (including owner) and create multiple channels...
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Tara', 'Andresson')
    token_owner = auth.auth_login('validemail@gmail.com', '123abc!@#')

    auth.auth_register('validemail1@gmail.com', '123abc!@#', 'Genine', 'Buggsies')
    token_1 = auth.auth_login('validemail1@gmail.com', '123abc!@#')

    auth.auth_register('validemail2@gmail.com', '1234abc!@#', 'Jess', 'Apples')
    token_2 = auth.auth_login('validemail2@gmail.com', '1234abc!@#')

    channel_1 = channels_create(token_1['token'], 'Hola_Seniora', True)
    channel_2 = channels_create(token_2['token'], 'ILoveIcecream', True)
    channel_3 = channels_create(token_1['token'], 'ImAnEngineer', False)
    channel_4 = channels_create(token_2['token'], 'HugsOnly', False)

    # (owner vs member of Flockr)
    assert channels_list(token_owner['token']) == [
    {'channel_id': channel_1['channel_id'], 'name': 'Hola_Seniora'},
    {'channel_id': channel_2['channel_id'], 'name': 'ILoveIcecream'},
    {'channel_id': channel_3['channel_id'], 'name': 'ImAnEngineer'},
    {'channel_id': channel_4['channel_id'], 'name': 'HugsOnly'}]

    assert channels_list(token_1['token']) == [
    {'channel_id': channel_1['channel_id'], 'name': 'Hola_Seniora'},
    {'channel_id': channel_3['channel_id'], 'name': 'ImAnEngineer'}]

    assert channels_list(token_2['token']) == [
    {'channel_id': channel_2['channel_id'], 'name': 'ILoveIcecream'},
    {'channel_id': channel_4['channel_id'], 'name': 'HugsOnly'}]

# ----- Fail List
def test_invalid_token():
    
    other.clear()
    
    # Register and login a user.
    auth.auth_register('validemail@gmail.com', 'password123', 'fname', 'lname')
    result = auth.auth_login('validemail@gmail.com', 'password123')
    
    # Create a channel with first user.
    channels_create(result['token'], 'channel_1', True)
    
    # Check that Access Error is raised when invalid token is used.
    with pytest.raises(AccessError):
        channels_list('fake_token')

