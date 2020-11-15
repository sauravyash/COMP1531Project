################################# User Fixtures ###############################
'''
Fixtures to remove repeated code and improve readability of testing.
'''

import pytest

import auth
import channels
import other

@pytest.fixture()
def setup_test_interface():
    ''' Setup_test_interface 
    Clear data, then register and login a single user.
    '''
    
    other.clear()
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    user = auth.auth_login('validemail@gmail.com', 'validpassword')

    return user
