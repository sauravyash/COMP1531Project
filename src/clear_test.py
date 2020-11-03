'''
import functions
'''
import auth
import channels
import other
from channel import channel_invite
from other import clear

# Success
# return the program to its orginal state
def test_user_all():
    '''
    Test if the clear function return the system to its original state
    '''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("good_email@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("good_email@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel_invite(result["token"], channel_id["channel_id"], result1["u_id"])

    assert clear() == {}
