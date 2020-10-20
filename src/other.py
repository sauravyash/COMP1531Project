import data
from error import AccessError
from channels import channels_list

# Clears original data structure...
def clear():
    data.data = {
        'users': [],
        'channels': []
    }
    pass

def users_all(token):
    ''' Displays list of all users and respective data

    Arguments: token, must be string
    Returns: list of users
    '''
    try:
        data.resolve_token(token)
    except LookupError:
        raise AccessError("Token not found")

    return {
        data.data["users"]
    }
#    return {
#        'users': [
#            {
#                'u_id': 1,
#                'email': 'cs1531@cse.unsw.edu.au',
#                'name_first': 'Hayden',
#                'name_last': 'Jacobs',
#                'handle_str': 'hjacobs',
#            },
#        ],
#    }

def admin_userpermission_change(token, u_id, permission_id):
    pass

def search(token, query_str):
    
    list_of_messages = []
    list_of_channels = channels_list(token)
    
    # Go through the relevant channels...
    for channel in list_of_channels:
        index = data.resolve_channel_id_index(channel['channel_id'])
        # Test if the user is a member or admin of the channel (has joined)
        selected_channel = data.data['channels'][index]
        if token in selected_channel['members'] or token in selected_channel['admins']:
            for message_info in selected_channel['messages']:
                if query_str in message['message']:
                    # if the query string is contained within a message, add that
                    # message and its details to a list.
                    list_of_messages.append(message_info)
    
    return {
        'messages': list_of_messages
    }
