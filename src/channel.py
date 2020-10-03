from error import AccessError
from error import InputError
import data
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


    return {}
    

def channel_removeowner(token, channel_id, u_id):
    return {
    }