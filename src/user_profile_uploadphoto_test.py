'''Import functions'''
import pytest
import auth
import other
from error import InputError
from error import AccessError
from user import user_profile_uploadphoto

####### NOTE ###########

#InputError- when img_url returns an HTTP status other than 200.

########################

def test_user_profile_uploadphoto():
    ''' Success upload photo'''
    other.clear()

    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("coolemail@gmail.com", "password123")

    assert(user_profile_uploadphoto(result["token"], "https://static.scientificamerican.com/sciam/cache/file/92E141F8-36E4-4331-BB2EE42AC8674DD3_source.jpg", 0, 0, 256, 256)) == {}


def test_not_jpg():
    ''' Image URL is not jpg'''
    other.clear()

    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("coolemail@gmail.com", "password123")

    with pytest.raises(InputError):
        user_profile_uploadphoto(result["token"], "https://upload.wikimedia.org/wikipedia/commons/6/6c/Star_Wars_Logo.svg", 0, 0, 256, 256)


def test_invalid_demension():
    '''Invalid Demension'''
    other.clear()

    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("coolemail@gmail.com", "password123")

    with pytest.raises(InputError):
        user_profile_uploadphoto(result["token"], "https://static.scientificamerican.com/sciam/cache/file/92E141F8-36E4-4331-BB2EE42AC8674DD3_source.jpg", -1, -1, 256, 256)
