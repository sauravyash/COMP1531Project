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
        raise InputError(description="Invalid Message")

    user_id = -1

    try:
        user_id = data.token_to_user_id(token)
    except:
        raise AccessError(description="Invalid token")

    try:
        channel_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError(description='Invalid Channel ID')

    if not data.resolve_permissions(channel_id, user_id):
        raise AccessError(description="User Not Permitted!")

    # create msg
    new_id = data.generate_message_id()

    msg = {
        'message_id': new_id,
        'u_id': user_id,
        'message': message,
        'time_created': datetime.datetime.now().timestamp(),
        'reacts': [],
        'is_pinned': False

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
        raise AccessError(description="invalid token")
    try:
        channel_id, msg_index = data.resolve_message_id_index(message_id)
        channel_index = data.resolve_channel_id_index(channel_id)
    except:
        raise InputError(description="invalid message or channel id")


    msgs = data.data.get('channels')[channel_index]['messages']

    is_user_author = msgs[msg_index]['u_id'] == user_id
    is_admin = data.resolve_permissions(channel_id, user_id) == 1
    if not is_user_author and not is_admin:
        raise AccessError(description="user not authorised")

    # remove msg from list
    msgs.pop(msg_index)

    return {}

def message_edit(token, message_id, message):
    if not is_message_valid(message):
        raise InputError(description="Invalid Message")

    channel_id, channel_index, msg_index = (-1, -1, -1)

    try:
        user_id = data.token_to_user_id(token)
    except:
        raise AccessError(description="invalid token")

    try:
        channel_id, msg_index = data.resolve_message_id_index(message_id)
        channel_index = data.resolve_channel_id_index(channel_id)
    except:
        raise InputError(description="invalid message or channel id")

    msgs = data.data.get('channels')[channel_index]['messages']

    is_user_author = msgs[msg_index]['u_id'] == user_id
    is_admin = data.resolve_permissions(channel_id, user_id) == 1
    if not is_user_author and not is_admin:
        raise AccessError(description="user not authorised")

    data.print_data()
    msgs[msg_index]['message'] = message

    return {}

def message_sendlater(token, channel_id, message, time_send):
    ''' stub '''
    if time_send < datetime.datetime.now().timestamp():
        raise InputError(description="Time sent is a time in the past")

    # check permissions
    if not is_message_valid(message):
        raise InputError(description="Invalid Message: contents too long")

    user_id = -1

    try:
        user_id = data.token_to_user_id(token)
    except: # pragma: no cover
        raise AccessError(description="Invalid token")

    try:
        channel_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError(description='Invalid Channel ID')

    if not data.resolve_permissions(channel_id, user_id):
        raise AccessError(description="User Not Permitted!")

    # create msg
    new_id = data.generate_message_id()

    msg = {
        'message_id': new_id,
        'u_id': user_id,
        'message': message,
        'time_created': time_send,
        'reacts': [],
        'is_pinned': False

    }

    # add msg to data
    msgs = data.data.get('channels')[channel_index]['messages']
    msgs.append(msg)

    return {
        'message_id': msg['message_id'],
    }

def message_react(token, message_id, react_id):
    '''stub'''
    channel_id, channel_index, msg_index = (-1, -1, -1)
    if react_id != 1:
        raise InputError(description="Invalid React ID!")

    try:
        user_id = data.token_to_user_id(token)
    except: # pragma: no cover
        raise AccessError(description="invalid token")

    try:
        channel_id, msg_index = data.resolve_message_id_index(message_id)
        channel_index = data.resolve_channel_id_index(channel_id)
    except:
        raise InputError(description="invalid message or channel id")

    msg = data.data['channels'][channel_index]['messages'][msg_index]
    data.print_data()

    if react_id not in [r['react_id'] for r in msg['reacts']]:
        msg['reacts'].append({
            'react_id': react_id,
            'u_ids': [user_id]
        })
    else:
        for i, react in enumerate(msg['reacts']): # pragma: no cover
            if react['react_id'] == react_id:
                if user_id not in react['u_ids']:
                    msg['reacts'][i]['u_ids'].append(user_id)
                else:
                    raise InputError(description="User Already Reacted to Message!")

    return {}


def message_unreact(token, message_id, react_id):
    '''stub'''
    channel_id, channel_index, msg_index = (-1, -1, -1)
    if react_id != 1:
        raise InputError(description="Invalid React ID!")

    try:
        user_id = data.token_to_user_id(token)
    except: # pragma: no cover
        raise AccessError(description="invalid token")

    try:
        channel_id, msg_index = data.resolve_message_id_index(message_id)
        channel_index = data.resolve_channel_id_index(channel_id)
    except:
        raise InputError(description="invalid message or channel id")

    msg = data.data['channels'][channel_index]['messages'][msg_index]

    found_react = False
    for i, react in enumerate(msg['reacts']):
        if react['react_id'] == react_id: # pragma: no cover
            found_react = True
            if user_id in react['u_ids']:
                 msg['reacts'][i]['u_ids'].remove(user_id)
            else:
                raise InputError(description="User Already Unreacted to Message!")
            break

    if not found_react:
        raise InputError(description="User Already Unreacted to Message!")
    return {}

def message_pin(token, message_id):
    '''stub'''
    channel_id, channel_index, msg_index = (-1, -1, -1)

    try:
        user_id = data.token_to_user_id(token)
    except: # pragma: no cover
        raise AccessError(description="invalid token")

    try:
        channel_id, msg_index = data.resolve_message_id_index(message_id)
        channel_index = data.resolve_channel_id_index(channel_id)
    except:
        raise InputError(description="invalid message or channel id")

    if data.resolve_permissions(channel_id, user_id) != 1:
        raise AccessError(description="User is not owner")

    msg = data.data['channels'][channel_index]['messages'][msg_index]

    if not msg['is_pinned']:
        msg['is_pinned'] = True
    else:
        raise InputError(description="Message is Already Pinned!")

    return {}

def message_unpin(token, message_id):
    '''stub'''
    channel_id, channel_index, msg_index = (-1, -1, -1)

    try:
        user_id = data.token_to_user_id(token)
    except: # pragma: no cover
        raise AccessError(description="invalid token")

    try:
        channel_id, msg_index = data.resolve_message_id_index(message_id)
        channel_index = data.resolve_channel_id_index(channel_id)
    except:
        raise InputError(description="invalid message or channel id")

    if data.resolve_permissions(channel_id, user_id) != 1:
        raise AccessError(description="User is not owner")

    msg = data.data['channels'][channel_index]['messages'][msg_index]

    if msg['is_pinned']:
        msg['is_pinned'] = False
    else:
        raise InputError(description="Message is Already Unpinned!")

    return {}
