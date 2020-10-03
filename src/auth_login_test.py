import auth
import other
import pytest
from error import InputError

#Successful logins
def test_success():
    other.clear()
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    auth.auth_login('validemail@gmail.com', 'validpassword')

#Unsuccesful logins
def test_unregistered_email():
    other.clear()
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    with pytest.raises(InputError) as e:
        auth.auth_login('unregisteredemail@gmail.com', 'validpassword')

def test_incorrect_password():
    other.clear()
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    with pytest.raises(InputError) as e:
        auth.auth_login('validemail@gmail.com', 'notthecorrectpassword')

def test_invalid_email():
    other.clear()
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    with pytest.raises(InputError) as e:
        auth.auth_login('invalidemail.com', 'validpassword')

def test_empty_email():
    other.clear()
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    with pytest.raises(InputError) as e:
        auth.auth_login('', 'validpassword')

def test_empty_password():
    other.clear()
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    with pytest.raises(InputError) as e:
        auth.auth_login('validemail@gmail.com', '')
