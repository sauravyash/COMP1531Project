'''
Functions to test http server auth functionality
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

from testing_fixtures.http_test_fixtures import url, setup_auth
from testing_fixtures.http_test_fixtures import register_user, login_user, logout_user

def test_url(url):
    '''Check server set up properly'''
    assert url.startswith("http")

# ---------------------------------------------------------------------------- #
''' ----- CHANNEL INVITE ----- '''


''' ----- CHANNELS DETAILS ----- '''


''' ----- CHANNELS MESSAGES ----- '''


''' ----- CHANNELS LEAVE ----- '''


''' ----- CHANNELS JOIN ----- '''


''' ----- CHANNELS ADDOWNER ----- '''


''' ----- CHANNELS REMOVEOWNER ----- '''
