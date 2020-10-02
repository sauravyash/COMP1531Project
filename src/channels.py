import data

def channels_list(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

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
