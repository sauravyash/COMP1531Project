import pytest

import auth
import channels
import other

@pytest.fixture()
def setup_test_interface():
    other.clear()

    # Register and login three users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    user1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    user2 = auth.auth_login('validemail2@gmail.com', 'password123')

    auth.auth_register('validemail3@gmail.com', 'password123', 'fname3', 'lname3')
    user3 = auth.auth_login('validemail3@gmail.com', 'password123')

    # Create a channel with the first user.
    channel_id = channels.channels_create(user1['token'], 'channel_1', True)
    
    return user1, user2, user3, channel_id
