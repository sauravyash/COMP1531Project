from auth import auth_register
from auth import auth_login
from auth import auth_logout
import pytest

#Successful logouts
def test_logout():
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    auth.auth_login('validemail@gmail.com', 'validpassword')
    auth.auth_logout(result[token])

#Unsuccesful logouts
def test_unregisteredemail():
    result = auth.auth_register('validemail1@gmail.com', 'validpassword', 'fname', 'fname')
    auth.auth_login('validemail1@gmail.com', 'validpassword')
    #invalid token (unvalidated token)
    auth.auth_logout(result[token])
