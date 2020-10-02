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
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create(token, name, is_public):
    channel_id = 0 
    data.data['channels'].append({
        'id': channel_id,
        'name' : name,
        'admins': [data.resolve_token(token)],
        'members': [] ,
        'messages' []
        'is_public': True
    })
    return {
        'channel_id': channel_id,
    }
