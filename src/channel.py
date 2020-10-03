import data
from error import AccessError
from error import InputError
def channel_invite(token, channel_id, u_id):
    return {
    }

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
    return {
    }

def channel_join(token, channel_id):

    u_id_index = 0
    channel_id_index = 0
    
    try:  
        channel_id_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError("Invalid channel ID")

    # member in the channel already
    for l in data.data['channels'][channel_id_index]['members']:
        if u_id == l:
            raise AccessError("Duplicate UserID")
    channel =  data.data['channels'][channel_id_index]            

    # append
    user = data.resolve_token(token)
    is_owner = data.data['users'][data.resolve_user_id_index(user)]['owner']
    if channel['is_public'] or is_owner == 'owner': 
        channel['members'].append(u_id)

 
    return {}


def channel_addowner(token, channel_id, u_id):
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }