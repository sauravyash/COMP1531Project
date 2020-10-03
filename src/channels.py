import data

from error import InputError

def channels_list(token):
    try:
        new_list = []
        
        # Find user_id by token...
        user_id = data.resolve_token(token)
        
        # Flockr owner can see all channels...
        for user in data.data['users']:
            if user['owner'] == 'owner' and user['id'] == user_id:
                channels_listall(token)           
        
        # Otherwise, only the channels they are a member of...
        for channel in data.data['channels']:
            for member in channel['members']:
                if u_id == member:
                    new_list.append({channel['id']: channel['name']})    
            for owner in channel['owners']:
                if u_id == owner:
                    new_list.append({channel['id'], channel['name']})
        
        return new_list
    
    # If token is invalid or empty..
    except:
        return []


def channels_listall(token):
    # Check if token exists...
    
    new_list = []
    
    for channel in data.data['channels']:
        new_list.append({channel['id']: channel['name']})   
    
    return new_list


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
