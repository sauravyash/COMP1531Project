############################# Standup Active Tests ###########################
'''
Functions to test standup_active functionality
'''

''' NOT YET IMPLEMENTED
import pytest
import other

from error import InputError, AccessError
from standup import standup_active, standup_start

from testing_fixtures.standup_test_fixtures import setup_test_interface

# ----- Success Active
def test_no_standup(setup_test_interface):
    user1, _, channel_id = setup_test_interface

    result_standup_active = standup_active(user1["token"],channel_id)
    assert len(result_standup_active) == 2
    assert standup_not_active['is_active'] == False
    assert standup_not_active['time_finish'] == None

def test_simple(setup_test_interface):
    user1, _, channel_id = setup_test_interface

    # Initially standup is not active
    standup_not_active = standup_active(user1["token"],channel_id)
    assert standup_not_active['is_active'] == False
    # Start a standup and store value for finishing time.
    standup_started = standup_active(user1['token'], channel_id)
    # Now standup is active and finish times should match.
    standup_is_active = standup_active(user1["token"],channel_id)
    assert standup_is_active['is_active'] == True
    assert standup_is_active['time_finish'] == standup_started['time_finish']

# ----- Fail Active
def test_invalid_token(setup_test_interface):
    _, _, channel_id = setup_test_interface

    with pytest.raises(AccessError):
        standup_active(-999, channel_id)
    with pytest.raises(AccessError):
        standup_active('fake_token', channel_id)

def test_invalid_channel_id(setup_test_interface):
    user1, _, _ = setup_test_interface

    with pytest.raises(InputError):
        standup_active(user1["token"], -999)
    with pytest.raises(InputError):
        standup_active(user1["token"], 'fake_channel')
''' 
