import data
from error import InputError

def channels_create(token, name, is_public):
    if not isinstance(token, str) or len(token) < 1:
        raise InputError("Invalid Token")
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
