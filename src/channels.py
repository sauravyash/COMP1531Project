import data

from error import InputError
from error import AccessError

def channels_list(token):

    new_list = []

    try:
        # Find user_id by token...
        user_id = data.resolve_token(token)
    except:
        print("Something is not right...")
        return new_list

    # Flockr owner can see all channels...
    for user in data.data['users']:
        if user['flockr_owner'] and user['id'] == user_id:
            return channels_listall(token)

    # Otherwise, only the channels they are a member of...
    for channel in data.data['channels']:
        for member in channel['members']: # pragma: no cover
            if user_id == member:
                new_list.append(
                    {'channel_id': channel['id'], 'name': channel['name']})
        for admin in channel['admins']:
            if user_id == admin:
                new_list.append(
                    {'channel_id': channel['id'], 'name': channel['name']})

    return new_list

def channels_listall(token):

    # Check that token is valid, if so return list of all channels...
    try:
        new_list = []
        data.resolve_token(token)

        for channel in data.data['channels']:
            new_list.append(
                {
                    'channel_id': channel['id'],
                    'name': channel['name'],
                })

        return new_list

    # If token doesn't exist, return empty list...
    except:
        return []

def channels_create(token, name, is_public):
    
    # Check that token exists/ is valid.
    try:
        data.resolve_token(token)
    except LookupError: # pragma: no cover
        raise AccessError("Invalid Token")
    
    # Check if name param is valid.
    if not isinstance(name, str) or len(name) > 20 or len(name) < 1:
        raise InputError("Invalid Name")
    # Check if is_public param is valid.
    if not isinstance(is_public, bool):
        raise InputError("Invalid is_public variable")
    
    # Create and check that channel id is unique... (to be fixed)
    channel_id = 0
    unique = False
    while not unique:
        try:
            data.resolve_channel_id_index(channel_id)
            channel_id += 1
        except LookupError:
            unique = True

    # Create channel data structure & add new information...
    data.data['channels'].append({
        'id': channel_id,
        'name' : name,
        'members': {
            'permission_id_1': [data.resolve_token(token)],
            'permission_id_2': [],
        }
        'messages': [],
        'is_public': is_public
    })
    
    return {
        'channel_id': channel_id,
    }
