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
    