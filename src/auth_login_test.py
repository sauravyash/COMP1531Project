import auth
import other
import pytest
from error import InputError

#Successful logins
def test_validemail():
    other.clear()
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    auth.auth_login('validemail@gmail.com', 'validpassword')

#Unsuccesful logins
def test_unregisteredemail():
    other.clear()
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    with pytest.raises(InputError) as e:
        auth.auth_login('unregisteredemail@gmail.com', 'validpassword')

def test_incorrectpassword():
    other.clear()
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    with pytest.raises(InputError) as e:
        auth.auth_login('validemail@gmail.com', 'notthecorrectpassword')

def test_invalidemail():
    other.clear()
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    with pytest.raises(InputError) as e:
        auth.auth_login('invalidemail.com', 'validpassword')
