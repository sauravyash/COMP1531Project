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
    for l in data.data['channels'][channel_id_index]['members']:
        if u_id == l:
            raise AccessError("Duplicate UserID")
                

    # append
    data.data['channels'][channel_id_index]['members'].append(u_id)
 
    return {}

def channel_details(token, channel_id):
    channel_id_index = data.resolve_channel_id_index(channel_id)
    
    channel = data.data['channels'][channel_id_index]
    users = channel['admins'] + channel['members']
    
    if data.resolve_token(token) not in users:
        raise AccessError("Not a member of the specified channel")
    
    return channel


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
    u_id_index = 0
    channel_id_index = 0
    u_id = 0
    try: 
        
        channel_id_index = data.resolve_channel_id_index(channel_id)
       

    except LookupError:
        raise InputError("Invalid channel ID")

    # user
    try:
        u_id = data.resolve_token(token)
        u_id_index = data.resolve_user_id_index(u_id)

    except LookupError:
        raise InputError("Invalid token")

    # remove
    data.data['channels'][channel_id_index]['members'].remove(u_id)

    return {}

def channel_join(token, channel_id):
    u_id_index = 0
    channel_id_index = 0
    
    # channel
    try:         
        channel_id_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError("Invalid channel ID")

    # user
    try:
        u_id_index = data.resolve_user_id_index(u_id)
    except LookupError:
        raise InputError("Invalid user ID")


    data.data['channels'][channel_id_index]['admins'].append(u_id)

    return {
    }

def channel_addowner(token, channel_id, u_id):
    u_id_index = 0
    channel_id_index = 0
    
    # channel
    try:         
        channel_id_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError("Invalid channel ID")

    # user
    try:
        u_id_index = data.resolve_user_id_index(u_id)
    except LookupError:
        raise InputError("Invalid user ID")


    data.data['channels'][channel_id_index]['admins'].append(u_id)

    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }
