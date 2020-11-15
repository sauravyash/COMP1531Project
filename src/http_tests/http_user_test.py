############################ Http User Server Tests ##########################
'''
Functions to test http server user functionality
'''

from subprocess import Popen, PIPE
from time import sleep
import json
import urllib
import re
import signal
import requests
import logging
import pytest

from data import print_data

from testing_fixtures.http_test_fixtures import url, setup_auth, login_user, register_user

def test_url(url):
    '''Check server set up properly'''
    assert url.startswith("http")

# ---------------------------------------------------------------------------- #
''' ----- USER SET EMAIL ----- '''

def test_valid_email_change(url, login_user):

    user1, _, _ = login_user

    input_data = {
        "token": user1["token"],
        "email": "newvalidemail@gmail.com"
    }

    data = requests.put(f"{url}/user/profile/setemail", json=input_data)

    assert data.status_code == 200

def test_invalid_email_change(url, login_user):

    user1, _, _ = login_user

    input_data = {
        "token": user1["token"],
        "email": "notvalidemail.com"
    }

    data = requests.put(f"{url}/user/profile/setemail", json=input_data)

    assert data.status_code == 401

''' ----- USER SET NAME ----- '''
def test_valid_name_change(url, login_user):

    user1, _, _ = login_user

    input_data = {
        "token": user1["token"],
        "name_first": "newfname",
        "name_last": "newlname"
    }

    data = requests.put(f"{url}/user/profile/setname", json=input_data)

    assert data.status_code == 200

def test_invalid_fname_change(url, login_user):

    user1, _, _ = login_user

    input_data = {
        "token": user1["token"],
        "name_first": "",
        "name_last": "newlname"
    }

    data = requests.put(f"{url}/user/profile/setname", json=input_data)

    assert data.status_code == 401

    input_data = {
        "token": user1["token"],
        "name_first": "newfirstnamewhichiscertainlymorethanfiftycharacterslong",
        "name_last": "newlname"
    }

    data = requests.put(f"{url}/user/profile/setname", json=input_data)

    assert data.status_code == 401

def test_invalid_lname_change(url, login_user):

    user1, _, _ = login_user

    input_data = {
        "token": user1["token"],
        "name_first": "newfname",
        "name_last": ""
    }

    data = requests.put(f"{url}/user/profile/setname", json=input_data)

    assert data.status_code == 401

    input_data = {
        "token": user1["token"],
        "name_first": "newfname",
        "name_last": "newfirstnamewhichiscertainlymorethanfiftycharacterslong"
    }

    data = requests.put(f"{url}/user/profile/setname", json=input_data)

    assert data.status_code == 401

''' ----- USER SET HANDLE ----- '''
def test_valid_handle_change(url, login_user):
    user1, _, _ = login_user

    input_data = {
        "token": user1["token"],
        "handle_str": "newhandle"
    }

    data = requests.put(f"{url}/user/profile/sethandle", json=input_data)

    assert data.status_code == 200

def test_invalid_handle_short(url, login_user):
    user1, _, _ = login_user

    input_data = {
        "token": user1["token"],
        "handle_str": "ah"
    }

    data = requests.put(f"{url}/user/profile/sethandle", json=input_data)

    assert data.status_code == 401

def test_invalid_handle_long(url, login_user):
    user1, _, _ = login_user

    input_data = {
        "token": user1["token"],
        "handle_str": "handlehasmorethantwentycharacters"
    }

    data = requests.put(f"{url}/user/profile/sethandle", json=input_data)

    assert data.status_code == 401

''' ----- USER UPLOAD PHOTO ----- '''
def test_valid_uploadphoto(url, login_user):
    user1, _, _ = login_user

    input_data = {
        "token": user1["token"],
        "img_url": "https://i.pinimg.com/originals/23/04/a1/2304a18385e790a38b686de96196e305.jpg",
        "x_start": 50,
        "y_start": 100,
        "x_end": 250,
        "y_end": 300
    }

    data = requests.post(f"{url}/user/profile/uploadphoto", json=input_data)

    assert data.status_code == 200

def test_invalid_uploadphoto(url, login_user):
    user1, _, _ = login_user

    input_data = {
        "token": user1["token"],
        "img_url": "https://upload.wikimedia.org/wikipedia/en/f/fd/Pusheen_the_Cat.png",
        "x_start": 50,
        "y_start": 100,
        "x_end": 250,
        "y_end": 300
    }

    data = requests.post(f"{url}/user/profile/uploadphoto", json=input_data)

    assert data.status_code == 401
