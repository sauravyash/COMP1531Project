import pytest

import auth
import channels
import other

@pytest.fixture()
def setup_test_interface():
    other.clear()

    # Register and login two users.
    auth.auth_register('validemail1@gmail.com', 'password123', 'fname1', 'lname1')
    user1 = auth.auth_login('validemail1@gmail.com', 'password123')

    auth.auth_register('validemail2@gmail.com', 'password123', 'fname2', 'lname2')
    user2 = auth.auth_login('validemail2@gmail.com', 'password123')

    # Create a channel with the first user.
    channel_id = channels.channels_create(user1['token'], 'channel_1', True)
    
    return user1, user2, channel_id['channel_id']
