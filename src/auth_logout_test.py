import auth
import other
import pytest
from error import AccessError

#Successful logouts
def test_logout():
    other.clear()
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    auth.auth_login('validemail@gmail.com', 'validpassword')
    assert(auth.auth_logout(result["token"])["is_success"] == True)

#Unsuccesful logouts
def test_already_logged_out():
    other.clear()
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    auth.auth_login('validemail@gmail.com', 'validpassword')
    auth.auth_logout(result["token"])
    #invalid token (unvalidated token)
    assert(auth.auth_logout(result["token"])["is_success"] == False)

def test_invalid_token():
    other.clear()
    result = auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    auth.auth_login('validemail@gmail.com', 'validpassword')

    with pytest.raises(AccessError):
        auth.auth_logout("Invalid token")
