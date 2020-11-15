################################# Auth Fixtures ###############################
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
    Clear the data, then register and login one user.
    '''
    other.clear()
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    user = auth.auth_login('validemail@gmail.com', 'validpassword')

    return user
