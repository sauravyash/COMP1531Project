############################## Standup Start Tests ############################
'''
Functions to test standup_start functionality
'''

import pytest
import other
import datetime
import time

from error import InputError, AccessError
from standup import standup_start, standup_active

from testing_fixtures.standup_test_fixtures import setup_test_interface

# ----- Success Start
# Not a lot of methods for testing whether standup works on its own.
def test_simple(setup_test_interface):
    user1, _, channel_id = setup_test_interface
    
    # Test standup start returns correct types.
    standup_dict = standup_start(user1["token"], channel_id, 5)
    assert len(standup_dict) == 1
    assert isinstance(standup_dict, dict)
    assert isinstance(standup_dict['time_finish'], float)
    
    # Test standup information and activity is carried across other functions.
    standup_info = standup_active(user1['token'], channel_id)
    assert standup_info['is_active'] == True
    assert standup_info['time_finish'] == standup_dict['time_finish']
    
    time.sleep(5)
    
    # Test that standup has now ended.
    standup_info = standup_active(user1['token'], channel_id)
    assert standup_info['is_active'] == False
    assert standup_info['time_finish'] == None

# ----- Fail Start
def test_invalid_token(setup_test_interface):
    _, _, channel_id = setup_test_interface

    with pytest.raises(AccessError):
        standup_start(-999, channel_id, 100)
    with pytest.raises(AccessError):
        standup_start('fake_token', channel_id, 100)

def test_invalid_channel_id(setup_test_interface):
    user1, _, _ = setup_test_interface

    with pytest.raises(InputError):
        standup_start(user1["token"], -999, 100)
    with pytest.raises(InputError):
        standup_start(user1["token"], 'fake_channel', 100)

def test_standup_already_exists(setup_test_interface):
    user1, _, channel_id = setup_test_interface

    standup_start(user1["token"],channel_id, 100)

    with pytest.raises(InputError):
        standup_start(user1["token"],channel_id, 1)

