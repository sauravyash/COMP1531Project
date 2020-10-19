import pytest
import auth
import other
from user import user_profile
from error import InputError
from error import AccessError


# Success user_profile
#def test_valid_user_profile(): can't be blackbox?
#    other.clear()
#    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
#    result = auth.auth_login("validemail@gmail.com", "password123")


# When the token is valid but the user id is invalid
def test_invalid_user_profile():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    with pytest.raises(InputError):
        user_profile(result["token"], 0)


# When the user ID is valid but token is invalid
def test_invalid_user_profile_token():
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    with pytest.raises(AccessError):
        user_profile("INVALID TOKEN", result['u_id'])
