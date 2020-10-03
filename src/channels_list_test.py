import pytest

import data
import channels
import auth

from other import clear

### BLACKBOX TESTING ###

# Test function output types
# - channel_id is an int
# - name is a string
def test_channels_list_check_return_types():
    # Clear existing data...
    clear()
    
    assert isinstance(channels.channels_listall(""), list)
    
    for dictionary in channels.channels_listall(""):
        assert isinstance(dictionary, dict)
     
    # Set up user and create channel...
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Tara', 'Andresson')
    token_dict = auth.auth_login('validemail@gmail.com', '123abc!@#')
    channel_1 = channels.channels_create(token_dict['token'], 'Hola_Seniora', True)
    
    for dictionary in channels.channels_list(token_dict['token']):
        assert isinstance(dictionary['channel_id'], int)
        assert isinstance(dictionary['name'], str)


# Test empty list (no channels)
def test_channels_list_empty_list():
    # Clear existing data...
    clear()
    
    assert channels.channels_list("") == []


# Test list of many channels (for when we implement other functions)
def test_channels_list_public_only():
    # Clear existing data...
    clear()
    
    # Set up user and create a channel...
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Tara', 'Andresson')
    token_dict = auth.auth_login('validemail@gmail.com', '123abc!@#')
    channel_1 = channels.channels_create(token_dict['token'], 'Hola_Seniora', True)
    channel_2 = channels.channels_create(token_dict['token'], 'ILoveIcecream', True)
    
    # (Only public)
    assert channels.channels_list(token_dict['token']) == [
    {'channel_id': channel_1['channel_id'], 'name': 'Hola_Seniora'}, 
    {'channel_id': channel_2['channel_id'], 'name': 'ILoveIcecream'}]


def test_channels_list_public_private():    
    # Clear data
    clear()
    
    # Set up 3 users and create multiple channels...
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Tara', 'Andresson')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    
    auth.auth_register('validemail1@gmail.com', '123abc!@#', 'Genine', 'Buggsies')
    token_1 = auth.auth_login('validemail1@gmail.com', '123abc!@#')
    
    auth.auth_register('validemail2@gmail.com', '1234abc!@#', 'Jess', 'Apples')
    token_2 = auth.auth_login('validemail2@gmail.com', '1234abc!@#')
    
    channel_1 = channels.channels_create(token_1['token'], 'Hola_Seniora', True)
    channel_2 = channels.channels_create(token_2['token'], 'ILoveIcecream', True)
    channel_3 = channels.channels_create(token_1['token'], 'ImAnEngineer', False)
    channel_4 = channels.channels_create(token_2['token'], 'HugsOnly', False)
    
    # (Public & private)
    assert channels.channels_list(token_1['token']) == [
    {'channel_id': channel_1['channel_id'], 'name': 'Hola_Seniora'}, 
    {'channel_id': channel_3['channel_id'], 'name': 'ImAnEngineer'}]
    
    assert channels.channels_list(token_2['token']) == [
    {'channel_id': channel_2['channel_id'], 'name': 'ILoveIcecream'}, 
    {'channel_id': channel_4['channel_id'], 'name': 'HugsOnly'}]


def test_channels_list_owner_priv():    
    # Clear data
    clear()
    
    # Set up 3 users (including owner) and create multiple channels...
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Tara', 'Andresson')
    token_owner = auth.auth_login('validemail@gmail.com', '123abc!@#')
    
    auth.auth_register('validemail1@gmail.com', '123abc!@#', 'Genine', 'Buggsies')
    token_1 = auth.auth_login('validemail1@gmail.com', '123abc!@#')
    
    auth.auth_register('validemail2@gmail.com', '1234abc!@#', 'Jess', 'Apples')
    token_2 = auth.auth_login('validemail2@gmail.com', '1234abc!@#')
    
    channel_1 = channels.channels_create(token_1['token'], 'Hola_Seniora', True)
    channel_2 = channels.channels_create(token_2['token'], 'ILoveIcecream', True)
    channel_3 = channels.channels_create(token_1['token'], 'ImAnEngineer', False)
    channel_4 = channels.channels_create(token_2['token'], 'HugsOnly', False)
    
    # (owner vs member of Flockr)
    assert channels.channels_list(token_owner['token']) == [
    {'channel_id': channel_1['channel_id'], 'name': 'Hola_Seniora'},
    {'channel_id': channel_2['channel_id'], 'name': 'ILoveIcecream'}, 
    {'channel_id': channel_3['channel_id'], 'name': 'ImAnEngineer'}, 
    {'channel_id': channel_4['channel_id'], 'name': 'HugsOnly'}]
    
    assert channels.channels_list(token_1['token']) == [
    {'channel_id': channel_1['channel_id'], 'name': 'Hola_Seniora'}, 
    {'channel_id': channel_3['channel_id'], 'name': 'ImAnEngineer'}]
    
    assert channels.channels_list(token_2['token']) == [
    {'channel_id': channel_2['channel_id'], 'name': 'ILoveIcecream'}, 
    {'channel_id': channel_4['channel_id'], 'name': 'HugsOnly'}]


