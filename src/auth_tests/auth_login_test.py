############################### Auth Login Tests #############################
'''
Functions to test auth_login functionality
'''

import auth
import other
import pytest
from error import InputError
#from testing_fixtures.auth_test_fixtures import setup_test_interface_register

# ----- Successful logins
def test_success():
    '''
    Success login
    Valid email
    Valid password
    '''
    other.clear()
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    #user = setup_test_interface_register
    auth.auth_login('validemail@gmail.com', 'validpassword')

# ----- Unsuccesful logins
def test_unregistered_email():
    '''
    Unsuccesful login
    Invalid email (unregistered email)
    '''
    other.clear()
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    with pytest.raises(InputError):
        auth.auth_login('unregisteredemail@gmail.com', 'validpassword')

def test_incorrect_password():
    '''
    Unsuccesful login
    Invalid password
    '''
    other.clear()
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    with pytest.raises(InputError):
        auth.auth_login('validemail@gmail.com', 'notthecorrectpassword')

def test_invalid_email():
    '''
    Unsuccesful login
    Invalid email (invalid email format)
    '''
    other.clear()
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    with pytest.raises(InputError):
        auth.auth_login('invalidemail.com', 'validpassword')

def test_empty_email():
    '''
    Unsuccesful login
    Invalid email (empty email)
    '''
    other.clear()
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    with pytest.raises(InputError):
        auth.auth_login('', 'validpassword')

def test_empty_password():
    '''
    Unsuccesful login
    Invalid password (empty password)
    '''
    other.clear()
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    with pytest.raises(InputError):
        auth.auth_login('validemail@gmail.com', '')
