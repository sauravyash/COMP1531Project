'''Test Message's Functional Validity
'''

import data
import datetime
from error import InputError, AccessError

def is_message_valid(message):
    return isinstance(message, str) and len(message) <= 1000

def message_send(token, channel_id, message):
    
    # check permissions
    if not is_message_valid(message):
        raise InputError("Invalid Message")

    user_id = -1
    
    try:
        user_id = data.token_to_user_id(token)
    except:
        raise AccessError("Invalid token")

    try:
        channel_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError('Invalid Channel ID')

    if not data.resolve_permissions(channel_id, user_id):
        raise AccessError("User Not Permitted!")

    # create msg
    new_id = data.generate_message_id()

    msg = {
        'message_id': new_id,
        'u_id': user_id,
        'message': message,
        'time_created': datetime.datetime.now().timestamp()
    }

    # add msg to data
    msgs = data.data.get('channels')[channel_index]['messages']
    msgs.append(msg)

    return {
        'message_id': msg['message_id'],
    }

def message_remove(token, message_id):
    channel_id, user_id, channel_index, msg_index = tuple([-1 for _ in range(4)])

    try:
        user_id = data.token_to_user_id(token)
    except:
        raise AccessError("invalid token")
    try:    
        channel_id, msg_index = data.resolve_message_id_index(message_id)
        channel_index = data.resolve_channel_id_index(channel_id)
    except:
        raise InputError("invalid message or channel id")


    msgs = data.data.get('channels')[channel_index]['messages']
    
    is_user_author = msgs[msg_index]['u_id'] == user_id
    is_admin = data.resolve_permissions(channel_id, user_id) == 1
    if not is_user_author and not is_admin:
        raise AccessError("user not authorised")
    
    # remove msg from list
    msgs.pop(msg_index)

    return {}

def message_edit(token, message_id, message):
    if not is_message_valid(message):
        raise InputError("Invalid Message")

    channel_id, channel_index, msg_index = (-1, -1, -1)

    try:
        user_id = data.token_to_user_id(token)
    except:
        raise AccessError("invalid token")
    
    try:    
        channel_id, msg_index = data.resolve_message_id_index(message_id)
        channel_index = data.resolve_channel_id_index(channel_id)
    except:
        raise InputError("invalid message or channel id")

    msgs = data.data.get('channels')[channel_index]['messages']

    is_user_author = msgs[msg_index]['u_id'] == user_id
    is_admin = data.resolve_permissions(channel_id, user_id) == 1
    if not is_user_author and not is_admin:
        raise AccessError("user not authorised")
    
    data.print_data()
    msgs[msg_index]['message'] = message

    return {}

def message_sendlater(token, channel_id, messages, time_send):
    ''' stub '''
    return 0


def message_react(token, message_id, react_id):
    '''stub'''

    pass


def message_unreact(token, message_id, react_id):
    '''stub'''

    pass

def message_pin(token, message_id):
    '''stub'''
    pass

def message_unpin(token, message_id):
    '''stub'''
    pass
