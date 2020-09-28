from auth import auth_register
from auth import auth_login
import pytest

#Successful logins
def test_validemail():
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    auth.auth_login('validemail@gmail.com', 'validpassword')

#Unsuccesful logins
def test_unregisteredemail():
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    with pytest.raises(InputError) as e:
        auth_login('unregisteredemail@gmail.com', 'validpassword')

def test_incorrectpassword():
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    with pytest.raises(InputError) as e:
        auth_login('validemail@gmail.com', 'notthecorrectpassword')

def test_invalidemail():
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    with pytest.raises(InputError) as e:
        auth_login('invalidemail.com', 'validpassword')
