import pytest

import auth
import other

from channels import channels_create

@pytest.fixture()
def setup_test_interface_create():
    other.clear()

    # Register and login two users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    user1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    user2 = auth.auth_login('validemail2@gmail.com', 'password123')

    return user1, user2

@pytest.fixture()
def setup_test_interface_lists():
    other.clear()
    
    # Register and login three users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    user1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    user2 = auth.auth_login('validemail2@gmail.com', 'password123')
    
    auth.auth_register('validemail3@gmail.com', 'password123', 'fname3', 'lname3')
    user3 = auth.auth_login('validemail3@gmail.com', 'password123')
    
    users = []
    # List the users created
    users.append(user1)
    users.append(user2)
    users.append(user3)
    
    channels_1 = []
    channels_2 = []
    channels_3 = []
    # List the channels that each member has created.
    channels_1.append(channels_create(user1['token'], 'Hola_Seniora', True)['channel_id'])
    channels_2.append(channels_create(user2['token'], 'ILoveIcecream', True)['channel_id'])
    channels_3.append(channels_create(user3['token'], 'ImAnEngineer', True)['channel_id'])
    channels_1.append(channels_create(user1['token'], 'HugsOnly', False)['channel_id'])
    channels_2.append(channels_create(user2['token'], 'Hello-Puppys', False)['channel_id'])
    channels_2.append(channels_create(user2['token'], 'AlloChap', False)['channel_id'])

    return users, channels_1, channels_2, channels_3

