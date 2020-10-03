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

    try:
        new_list = []
        
        u_id = data.resolve_token(token)
        
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
    return {
        'channel_id': 1,
    }
