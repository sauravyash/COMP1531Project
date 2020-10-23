''' Other.py
Functions that do not relate to the more specific purpose of managing 
authentication, a channel and multiple channels.
'''

import data

from error import AccessError
from channels import channels_list

def clear():
    ''' Clear
    Reset the data structure to a blank dictionary.

    Arguments: None
    Return: None

    '''
    data.data = {
        'users': [],
        'channels': []
    }
    pass

def users_all(token):
    ''' All Users
    Displays list of all users and respective data.

    Arguments: token, must be string
    Returns: list of users

    '''
    try:
        data.resolve_token(token)
    except:
        raise AccessError(description='Invalid Token')

    user_list = []

    for user in data.data['users']:
        user_list.append({
            'u_id': user['id'],
            'email': user['email'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'handle_str': user['handle'],
        })

    return {
        'users': user_list
    }

def admin_userpermission_change(token, u_id, permission_id):
    ''' User Permission Change
    Change a user's permissions based on params passed in.

    Arguments: token- must be valid int, u_id must be valid int, permission_id-
    must be valid int
    Return: Empty dictionary, {}

    '''
    # Check that user ID is valid.
    try:
        data.resolve_user_id_index(user_id)
    except LookupError:
        raise InputError(description='Invalid User ID')

    # Check that the permission_id is valid.
    valid_ids = [1, 2]
    if permission_id not in valid_ids:
        raise InputError(description='Invalid Permission ID')
    
    # Check that the token is valid.
    try:
        user_id_token = data.token_to_user_id(token)
    except:
        raise AccessError(description='Invalid Token')

    # Naming to avoid confusion
    changing_user = user_id
    owner_user = user_id_token

    # Check that the authorised user is a global owner (owner of flocker)
    owner_index = resolve_user_id_index(owner_user)
    if data.data['users'][owner_index]['permission_id'] == 2:
        raise AccessError(description='User Not Authorised With Flockr Owner Permissions')

    # Change user permissions:
    changing_index = resolve_user_id_index(changing_user)
    data.data['users'][changing_index]['permission_id'] = permission_id

    return {}

def search(token, query_str):
    ''' Search
    Search for part of a message using a query string.

    Arguments: token- must be valid int, query_str- must be valid string
    Return: List of all messages that match search

    '''
    # Test if token is valid, if so return list of channels the user is a
    # member of.
    try:
        list_of_channels = channels_list(token)
    except AccessError:
        raise AccessError(description='Invalid Token')

    list_of_messages = []

    # Go through the relevant channels.
    for channel in list_of_channels: 
        channel_index = data.resolve_channel_id_index(channel['id'])
        selected_channel = data.data['channels'][channel_index]

        # Search for message within 'messages' of each channel.
        for message_info in selected_channel['messages']:
            if query_str in message_info['message']:
                # if the query string is contained within a message, add that
                # message and its details to a list.
                list_of_messages.append(message_info)

    return {
        'messages': list_of_messages
    }
