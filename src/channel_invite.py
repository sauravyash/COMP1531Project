import data
from error import InputError
from error import AccessError
def channel_invite(token, channel_id, u_id):
    # use i instead cid to avoid confusion
    # channels -> first key -> id in the first key
    # channel
    u_id_index = 0
    channel_id_index = 0
    
    try: 
        
        channel_id_index = data.resolve_channel_id_index(channel_id)
       

    except LookupError:
        raise InputError("Invalid channel ID")

    # user
    try:
        u_id_index = data.resolve_user_id_index(u_id)

    except LookupError:
        raise InputError("Invalid user ID")

    # member in the channel already
    print(channel_id_index)
    for l in data.data['channels'][channel_id_index]['members']:
        if u_id == l:
            raise AccessError
                

    # append
    for i in data.data['channels']:
        if channel_id == i['id'] : 
            member_list = i['members']
            member_list.append(u_id)
 
    return {}
    