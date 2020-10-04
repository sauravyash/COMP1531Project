import data
from error import AccessError
from error import InputError
def channel_invite(token, channel_id, u_id):
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
    try:
        channel_id_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError("Invalid channel ID")

    channel = data.data['channels'][channel_id_index]
    users = channel['admins'] + channel['members']

    if not isinstance(channel_id, int) or channel_id < 0:
        raise InputError("Channel ID is not valid")

    if data.resolve_token(token) not in users and channel["is_public"]:
        raise AccessError("Not a member of the specified channel")

    return {
        'name': channel['name'],
        'owner_members': channel['admins'],
        'all_members': channel['members'],
    }


def channel_messages(token, channel_id, start):
    try:
        channel_id_index = data.resolve_channel_id_index(channel_id)
    except LookupError as e:
        raise InputError(e.message)

    channel = data.data['channels'][channel_id_index]
    users = channel['admins'] + channel['members']

    if data.resolve_token(token) not in users:
        raise AccessError("Not a member of the specified channel")

    messages = channel['messages']

    if start > len(messages):
        raise InputError("Start is Out of Bounds")

    end = start + 50 if len(messages) >= 50 else -1

    return {
        'messages': messages[start::end],
        'start': start,
        'end': end,
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
    if u_id in data.data['channels'][channel_id_index]['members']:
        data.data['channels'][channel_id_index]['members'].remove(u_id)
    else:
        raise AccessError("User not in a member")

    return {}

def channel_join(token, channel_id):
    u_id_index = 0
    channel_id_index = 0

    try:
        channel_id_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError("Invalid channel ID")

    u_id = data.resolve_token(token)

    # member in the channel already
    for l in data.data['channels'][channel_id_index]['members']:
        if u_id == l:
            raise AccessError("Duplicate UserID")
    channel =  data.data['channels'][channel_id_index]

    # append
    user = data.resolve_token(token)
    is_owner = data.data['users'][data.resolve_user_id_index(user)]['owner']
    if channel['is_public'] or is_owner == 'owner':
        channel['members'].append(user)
    else:
        raise AccessError("Not authorized")

    return {}

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

    # user id from token
    user = data.resolve_token(token)
    is_owner = data.data['users'][data.resolve_user_id_index(user)]['owner']
    if is_owner != 'owner':
        raise AccessError("Not an owner of the specified channel")

    # user id from parameter
    is_owner = data.data['users'][data.resolve_user_id_index(u_id)]['owner'] 
    if is_owner == 'owner':
        raise AccessError("Target user already an owner of the channel")

    data.data['channels'][channel_id_index]['admins'].append(u_id)

    return {
    }

def channel_removeowner(token, channel_id, u_id):
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

    # user id from parameter
    # remove a member that is not owner
    is_owner = data.data['users'][data.resolve_user_id_index(u_id)]['owner'] 
    if is_owner != 'owner':
        raise InputError("Target user already an owner of the channel")

    # user id from token
    # remove not from owner
    user = data.resolve_token(token)
    is_owner = data.data['users'][data.resolve_user_id_index(user)]['owner']
    if is_owner != 'owner':
        raise AccessError("Not an owner of the specified channel")


    data.data['channels'][channel_id_index]['admins'].remove(u_id)

    return {
    }
