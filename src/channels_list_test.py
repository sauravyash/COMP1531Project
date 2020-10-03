import pytest

import channels
import auth
# from data file import global dictionary - for when we merge and implement

### BLACKBOX TESTING ###

# Test function output types
# - channel_id is an int
# - name is a string
def test_channels_list_check_return_types():
    assert isinstance(channels.channels_list(""), list)
    
    for dictionary in channels.channels_list(""):
        assert isinstance(dictionary, dict)
    
    # Testing for when other functions are implemented...
    '''   
    # Set up user and create channel...
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Tara', 'Andresson')
    token = auth.auth_login('validemail@gmail.com', '123abc!@#')
    channel_1 = channels.channels_create(token, 'Hola_Seniora', True)
    
    for dictionary in channels_list(token):
        assert isinstance(dictionary['channel_id'], int)
        assert isinstance(dictionary['name'], str)
    
    clear()
    '''

# Test empty list (no channels)
def test_channels_list_empty_list():
    assert channels.channels_list("") == []

# Test list of many channels (for when we implement other functions)
'''
def test_channels_list_public_only():
    # Set up user and create a channel...
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Tara', 'Andresson')
    token = auth.auth_login('validemail@gmail.com', '123abc!@#')
    channel_1 = channels.channels_create(token, 'Hola_Seniora', True)
    channel_2 = channels.channels_create(token, 'ILoveIcecream', True)
    
    (Only public)
    assert channels.channels_list(token) == 
        [{'channel_id': channel_1, 'name': 'Hola_Seniora'},
        {'channel_id': channel_2, 'name': 'ILoveIcecream'}]
    
    # Clear data
    clear()

def test_channels_list_public_private():    
    # Set up 3 users and create multiple channels...
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Tara', 'Andresson')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    
    auth.auth_register('validemail1@gmail.com', '123abc!@#', 'Genine', 'Buggsies')
    token_1 = auth.auth_login('validemail1@gmail.com', '123abc!@#')
    
    auth.auth_register('validemail2@gmail.com', '1234abc!@#', 'Jess', 'Apples')
    token_2 = auth.auth_login('validemail2@gmail.com', '1234abc!@#')
    
    channel_1 = channels.channels_create(token_1, 'Hola_Seniora', True)
    channel_2 = channels.channels_create(token_2, 'ILoveIcecream', True)
    channel_3 = channels.channels_create(token_1, 'ImAnEngineer', False)
    channel_4 = channels.channels_create(token_2, 'HugsOnly', False)
    
    (Public & private)
    assert channels.channels_list(token_1) == 
    [{'channel_id': channel_1, 'name': 'Hola_Seniora'}, 
    {'channel_id': channel_3, 'name': 'ImAnEngineer'}]
    
    assert channels.channels_list(token_2) == 
    [{'channel_id': channel_2, 'name': 'ILoveIcecream'}, 
    {'channel_id': channel_4, 'name': 'HugsOnly'}]
    
    # Clear data
    clear()

def test_channels_list_owner_priv():    
    # Set up 3 users (including owner) and create multiple channels...
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Tara', 'Andresson')
    token_owner = auth.auth_login('validemail@gmail.com', '123abc!@#')
    
    auth.auth_register('validemail1@gmail.com', '123abc!@#', 'Genine', 'Buggsies')
    token_1 = auth.auth_login('validemail1@gmail.com', '123abc!@#')
    
    auth.auth_register('validemail2@gmail.com', '1234abc!@#', 'Jess', 'Apples')
    token_2 = auth.auth_login('validemail2@gmail.com', '1234abc!@#')
    
    channel_1 = channels.channels_create(token_1, 'Hola_Seniora', True)
    channel_2 = channels.channels_create(token_2, 'ILoveIcecream', True)
    channel_3 = channels.channels_create(token_1, 'ImAnEngineer', False)
    channel_4 = channels.channels_create(token_2, 'HugsOnly', False)
    
    (Public & private)
    assert channels.channels_list(token_owner) ==
    [{'channel_id': channel_1, 'name': 'Hola_Seniora'},
    {'channel_id': channel_2, 'name': 'ILoveIcecream'}, 
    {'channel_id': channel_3, 'name': 'ImAnEngineer'}, 
    {'channel_id': channel_4, 'name': 'HugsOnly'}]
    
    assert channels.channels_list(token_1) == 
    [{'channel_id': channel_1, 'name': 'Hola_Seniora'}, 
    {'channel_id': channel_3, 'name': 'ImAnEngineer'}]
    
    assert channels.channels_list(token_2) == 
    [{'channel_id': channel_2, 'name': 'ILoveIcecream'}, 
    {'channel_id': channel_4, 'name': 'HugsOnly'}]
    
    # Clear data
    clear()

'''

