import data
from error import InputError
from error import AccessError
def channel_leave(token, channel_id):
    check_valid_cid = 0
    for i in data.data['channels']:
        if channel_id == i['id']: 
            # valid channel
            check_valid_cid = 1
            break
         
    if check_valid_cid is not 1:
        raise InputError
        return

    # find the user id using token
    saved_uID = -99
    valid_token = 0
    
    for k in data.data['users']:
        if token == k['token']:
            valid_token = 1
            saved_uID = k['id']

    # valid token
    if valid_token != 1:
        raise InputError
        return

    check_channel_member = 0
    member_list = []
    for i in data.data['channels']:
        if channel_id == i['id'] : 
            member_list = i['members']

    for users in member_list:
        if saved_uID == users:
            check_channel_member = 1
            break

    if (check_channel_member != 1):
        raise AccessError


    # remove
    # print(saved_uID)
    for i in data.data['channels']:
        if channel_id == i['id'] : 
            member_list = i['members']
            member_list.remove(saved_uID)

    return 
