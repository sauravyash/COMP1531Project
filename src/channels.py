import data

def channels_list(token):
    new_list = []
    
    # Find user_id by token...
    user_id = 'Edit123Here'
    
    for channel in data.data['channels']:
        for member in channel['members']:
            if u_id == member:
                new_list.append({channel['id']: channel['name']})    
        for owner in channel['owners']:
            if u_id == owner:
                new_list.append({channel['id'], channel['name']})
    
    return new_list

def channels_listall(token):
    # Check if token exists...
    
    new_list = []
    
    for channel in data.data['channels']:
        new_list.append({channel['id']: channel['name']})   
    
    return new_list

def channels_create(token, name, is_public):
    return {
        'channel_id': 1,
    }
