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
        user_id = data.resolve_token(token)
    except LookupError: # pragma: no cover
        raise AccessError('Invalid Token')
    except:
        raise AccessError("invalid token")
    try:
        channel_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError('Invalid Channel ID')

    if not data.is_user_authorised(channel_id, user_id):
        raise AccessError("User Not Permitted!")

    # create msg
    new_id = next(data.generate_msg_id())

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
        'message_id': msg['message_id']
    }

def message_remove(token, message_id):
    channel_id, user_id, channel_index, msg_index = tuple([-1 for _ in range(4)])

    try:
        channel_id, msg_index = data.resolve_message_id_index(message_id)
        channel_index = data.resolve_channel_id_index(channel_id)
        user_id = data.resolve_token(token)
    except LookupError:
        raise InputError("invalid token")
    except:
        raise InputError("invalid token")

    msgs = data.data.get('channels')[channel_index]['messages']
    is_user_author = msgs[msg_index]['u_id'] == user_id
    is_user_channel_owner = user_id in data.data.get('channels')[channel_index]['admins']
    try:
        is_user_flockr_owner = user_id == data.data['users'][0]['user_id']
    except KeyError:
        is_user_flockr_owner = False

    if not is_user_author and not is_user_channel_owner and not is_user_flockr_owner:
        raise AccessError("user not authorised")

    # remove msg from list
    msgs.pop(msg_index)

    return {}

def message_edit(token, message_id, message):
    if not is_message_valid(message):
        raise InputError("Invalid Message")

    channel_id, channel_index, msg_index = (-1, -1, -1)
    try:
        channel_id, msg_index = data.resolve_message_id_index(message_id)
        channel_index = data.resolve_channel_id_index(channel_id)
        user_id = data.resolve_token(token)
    except LookupError:
        raise InputError("invalid token")
    except:
        raise InputError("invalid token")

    msgs = data.data.get('channels')[channel_index]['messages']
    is_user_author = msgs[msg_index]['u_id'] == user_id
    is_user_channel_owner = user_id in data.data.get('channels')[channel_index]['admins']
    try:
        is_user_flockr_owner = user_id == data.data['users'][0]['user_id']
    except KeyError:
        is_user_flockr_owner = False

    if not is_user_author and not is_user_channel_owner and not is_user_flockr_owner:
        raise AccessError("user not authorised")
    data.print_data()
    msgs[msg_index]['message'] = message

    return {}
