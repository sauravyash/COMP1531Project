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
        if user['flockr_owner'] == True and user['id'] == user_id:
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

    # If token doesn't exist...
    except:
        return []

def channels_create(token, name, is_public):
    try:
        data.resolve_token(token)
    except LookupError: # pragma: no cover
        raise AccessError("Invalid Token")
    if not isinstance(name, str) or len(name) > 20 or len(name) < 1:
        raise InputError("Invalid Name")
    if not isinstance(is_public, bool):
        raise InputError("Invalid is_public variable")

    channel_id = 0
    unique = False
    while unique == False:
        try:
            data.resolve_channel_id_index(channel_id)
            channel_id += 1
        except LookupError:
            unique = True

    data.data['channels'].append({
        'id': channel_id,
        'name' : name,
        'admins': [data.resolve_token(token)],
        'members': [],
        'messages': [],
        'is_public': is_public
    })
    return {
        'channel_id': channel_id,
    }
