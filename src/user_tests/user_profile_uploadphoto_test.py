'''Import functions'''
import pytest
import auth
import other
from error import InputError
from error import AccessError
from user import user_profile_uploadphoto
from testing_fixtures.user_test_fixtures import setup_test_interface

####### NOTE ###########

#InputError- when img_url returns an HTTP status other than 200.

########################

#def test_user_profile_uploadphoto(setup_test_interface):
    #''' Success upload photo'''
    #user = setup_test_interface

    #assert(user_profile_uploadphoto(user["token"], "https://static.scientificamerican.com/sciam/cache/file/92E141F8-36E4-4331-BB2EE42AC8674DD3_source.jpg", 0, 0, 256, 256)) == {}


def test_user_profile_uploadphoto():
    ''' Success upload photo'''
    other.clear()

    auth.auth_register("coolemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("coolemail@gmail.com", "password123")

    assert(user_profile_uploadphoto(result["token"], "https://static.scientificamerican.com/sciam/cache/file/92E141F8-36E4-4331-BB2EE42AC8674DD3_source.jpg", 0, 0, 256, 256)) == {}

def test_not_jpg(setup_test_interface):
    ''' Image URL is not jpg'''
    user = setup_test_interface

    with pytest.raises(InputError):
        user_profile_uploadphoto(user["token"], "https://upload.wikimedia.org/wikipedia/commons/6/6c/Star_Wars_Logo.svg", 0, 0, 256, 256)

def test_invalid_width_small_start(setup_test_interface):
    '''Invalid Dimension'''
    user = setup_test_interface

    with pytest.raises(InputError):
        user_profile_uploadphoto(user["token"], "https://static.scientificamerican.com/sciam/cache/file/92E141F8-36E4-4331-BB2EE42AC8674DD3_source.jpg", -1, 0, 256, 256)

def test_invalid_width_large_start(setup_test_interface):
    '''Invalid Dimension'''
    user = setup_test_interface

    with pytest.raises(InputError):
        user_profile_uploadphoto(user["token"], "https://static.scientificamerican.com/sciam/cache/file/92E141F8-36E4-4331-BB2EE42AC8674DD3_source.jpg", 10000000, 0, 256, 256)

def test_invalid_height_small_start(setup_test_interface):
    '''Invalid Dimension'''
    user = setup_test_interface

    with pytest.raises(InputError):
        user_profile_uploadphoto(user["token"], "https://static.scientificamerican.com/sciam/cache/file/92E141F8-36E4-4331-BB2EE42AC8674DD3_source.jpg", 0, -1, 256, 256)

def test_invalid_height_large_start(setup_test_interface):
    '''Invalid Dimension'''
    user = setup_test_interface

    with pytest.raises(InputError):
        user_profile_uploadphoto(user["token"], "https://static.scientificamerican.com/sciam/cache/file/92E141F8-36E4-4331-BB2EE42AC8674DD3_source.jpg", 0, 10000000, 256, 256)

def test_invalid_width_small_end(setup_test_interface):
    '''Invalid Dimension'''
    user = setup_test_interface

    with pytest.raises(InputError):
        user_profile_uploadphoto(user["token"], "https://static.scientificamerican.com/sciam/cache/file/92E141F8-36E4-4331-BB2EE42AC8674DD3_source.jpg", 0, 0, -1, 256)

def test_invalid_width_large_end(setup_test_interface):
    '''Invalid Dimension'''
    user = setup_test_interface

    with pytest.raises(InputError):
        user_profile_uploadphoto(user["token"], "https://static.scientificamerican.com/sciam/cache/file/92E141F8-36E4-4331-BB2EE42AC8674DD3_source.jpg", 0, 0, 10000000, 256)

def test_invalid_height_small_end(setup_test_interface):
    '''Invalid Dimension'''
    user = setup_test_interface

    with pytest.raises(InputError):
        user_profile_uploadphoto(user["token"], "https://static.scientificamerican.com/sciam/cache/file/92E141F8-36E4-4331-BB2EE42AC8674DD3_source.jpg", 0, 0, 256, -1)

def test_invalid_height_large_end(setup_test_interface):
    '''Invalid Dimension'''
    user = setup_test_interface

    with pytest.raises(InputError):
        user_profile_uploadphoto(user["token"], "https://static.scientificamerican.com/sciam/cache/file/92E141F8-36E4-4331-BB2EE42AC8674DD3_source.jpg", 0, 0, 256, 10000000)
