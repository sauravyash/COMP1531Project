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
        user_id = data.resolve_token(token)
    except LookupError:
        raise InputError('Invalid Token')

    if not data.is_user_authorised(channel_id, user_id):
        raise AccessError("User not Permitted!")

    # create msg
    new_id = data.generate_msg_id(channel_id)
    
    msg = {
        'id': new_id,
        'author': user_id,
        'content': message,
        'time': datetime.datetime.now().timestamp()
    }

    # add msg to data
    msgs = data.get('channels')[channel_index]['messages']
    msgs.append(msg)

    return {
        'message_id': msg['id']
    }

def message_remove(token, message_id):
    if not is_message_valid(message):
        raise InputError("Invalid Message")

    channel_id, user_id, channel_index, msg_index = -1
    try:
        channel_id, msg_index = resolve_message_id_index(message_id)
        channel_index = data.resolve_channel_id_index(channel_id)
        user_id = data.resolve_token(token)
    except LookupError:
        raise InputError("invalid token")
    
    msgs = data.data.get('channels')[channel_index]['messages']
    
    if msgs[msg_index]['author'] != user_id:
        raise AccessError("user not authorised")
    
    # remove msg from list
    msgs.pop(msg_index)

    return { }

def message_edit(token, message_id, message):
    if not is_message_valid(message):
        raise InputError("Invalid Message")

    channel_id, channel_index, msg_index = -1
    try:
        channel_id, msg_index = resolve_message_id_index(message_id)
        channel_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError("invalid token")
    
    msgs = data.get('channels')[channel_index]['messages']
    if msgs[msg_index]['author'] != user_id:
        raise AccessError("user not authorised")
    
    msgs[msg_index]['content'] = message

    return {}
