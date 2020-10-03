import auth
import pytest

#Successful logouts
def test_logout():
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    auth.auth_login('validemail@gmail.com', 'validpassword')
    assert(auth.auth_logout(result["token"])["is_success"] == True)

#Unsuccesful logouts
def test_alreadyloggedout():
    result = auth.auth_register('validemail1@gmail.com', 'validpassword', 'fname', 'fname')
    auth.auth_login('validemail1@gmail.com', 'validpassword')
    auth.auth_logout(result["token"])
    #invalid token (unvalidated token)
    assert(auth.auth_logout(result["token"])["is_success"] == False)
