'''
import functions
'''
import auth
import channels
import other
from channel import channel_invite
#from clear import clear


def clear():
    '''
    stub
    '''

# Success
# return the program to its orginal state
def test_user_all():
    '''
    test if the clear function return the system to its original state
    '''
    other.clear()
    auth.auth_register("validemail@gmail.com", "password123", "fname", "lname")
    result = auth.auth_login("validemail@gmail.com", "password123")

    auth.auth_register("good_email@gmail.com", "password123", "fname1", "lname1")
    result1 = auth.auth_login("good_email@gmail.com", "password123")

    auth.auth_register("good_email@gmail.com", "password123", "fname2", "lname2")
    result2 = auth.auth_login("awsome_email@gmail.com", "password123")

    auth.auth_register("good_email@gmail.com", "password123", "fname3", "lname3")
    result3 = auth.auth_login("super_awsome_email@gmail.com", "password123")

    channel_id = channels.channels_create(result["token"], "channel_1", True)
    channel_invite(result["token"], channel_id["channel_id"], result3["u_id"])

    channel_id = channels.channels_create(result["token"], "channel_2", True)
    channel_invite(result2["token"], channel_id["channel_id"], result1["u_id"])
    assert clear() == {}
