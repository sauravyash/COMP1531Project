import data
from error import InputError
from error import AccessError
def channel_invite(token, channel_id, u_id):
    # use i instead cid to avoid confusion
    # channels -> first key -> id in the first key
    # channel

    check_valid_cid = 0
    for i in data.data['channels']:
        if channel_id == i['id']: 
            # valid channel
            check_valid_cid = 1
            break

    if check_valid_cid is not 1:
        raise InputError
        return

    # user
    check_valid_user = 0
    for j in data.data['users']:
        if (u_id == j['id']) and (token == j['token']):
            # valid user
            check_valid_user = 1
            break

    if check_valid_user is not 1:
        raise InputError
        return

    # member in the channel already
    for k in data.data['channels']:
        for l in k['members']:
            if u_id == l:
                raise AccessError
                return
    
    
    # append
    for i in data.data['channels']:
        if channel_id == i['id'] : 
            member_list = i['members']
            member_list.append(u_id)
 
    return
    

def channel_details(token, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages(token, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

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

def channel_join(token, channel_id):
    return {
    }

def channel_addowner(token, channel_id, u_id):
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }