''' Auth login tests
This file contains all test cases for auth login function.

'''
import auth
import other
import pytest
from error import InputError

# ----- Successful logins
def test_success():
    other.clear()
    # Register and login a user
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    auth.auth_login('validemail@gmail.com', 'validpassword')

# ----- Unsuccesful logins
def test_unregistered_email():
    other.clear()
    # Register a user.
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    # Attempt to login with a different email.
    with pytest.raises(InputError):
        auth.auth_login('unregisteredemail@gmail.com', 'validpassword')

def test_incorrect_password():
    other.clear()
    # Register a user.
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    # Attempt to ligin with a different password.
    with pytest.raises(InputError):
        auth.auth_login('validemail@gmail.com', 'notthecorrectpassword')

def test_invalid_email():
    other.clear()
    # Register a user.
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    # Attempt to login with an invalid eamil format.
    with pytest.raises(InputError):
        auth.auth_login('invalidemail.com', 'validpassword')

def test_empty_email():
    other.clear()
    # Register a user.
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    # Attempt to login with an empty email.
    with pytest.raises(InputError):
        auth.auth_login('', 'validpassword')

def test_empty_password():
    other.clear()
    # Register a user.
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    # Attempt to login with an empty password.
    with pytest.raises(InputError):
        auth.auth_login('validemail@gmail.com', '')
