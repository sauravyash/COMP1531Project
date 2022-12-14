''' Channels.py
File that contains all functions related to channels.

'''

import data

from error import InputError
from error import AccessError

def channels_list(token):

    ''' Channels_list
    Checks that the user has access to a channel before listing- all public
    channels and only private channels they have joined.
    
    Arguments: Token- must be a valid JWT token string.
    Return: Provide a list of all channels (and their associated details) that 
    the authorised user is part of.

    '''

    new_list = []

    # Check that the token is valid.
    try:
        user_id = data.token_to_user_id(token)
    except:
        raise AccessError(description='Invalid Token')

    # Otherwise, only the channels they are a member of.
    for channel in data.data['channels']:
        for member in channel['members']['permission_id_2']:
            if user_id == member:
                new_list.append(
                    {'channel_id': channel['id'], 'name': channel['name']})
        for admin in channel['members']['permission_id_1']:
            if user_id == admin:
                new_list.append(
                    {'channel_id': channel['id'], 'name': channel['name']})

    return {
        'channels': new_list 
    }

def channels_listall(token):
    ''' Channels_listall
    All channels are listed regardless of user permissions.

    Arguments: Token- must be a valid int.
    Return: Provide a list of all channels (and their associated details).

    '''

    # Check that the token is valid.
    try:
        data.token_to_user_id(token)
    except:
        raise AccessError(description='Invalid Token')

    new_list = []

    for channel in data.data['channels']:
        new_list.append(
            {
                'channel_id': channel['id'],
                'name': channel['name'],
            })

    return {
        'channels': new_list 
    }

def channels_create(token, name, is_public):

    ''' Channels_create
    A new section of the data structure is created and information about the
    channel is added.

    Arguments: Token- must be a valid int, name- must be a valid string,
    is_public- boolean value that controls public/private setting of channel.
    Return: Creates a new channel with that name that is either a public or
    private channel.
    '''

    # Check that token exists/ is valid.
    try:
        data.token_to_user_id(token)
    except: # pragma: no cover
        raise AccessError(description="Invalid Token")

    # Check if name param is valid.
    if not isinstance(name, str) or len(name) > 20 or len(name) < 1:
        raise InputError(description="Invalid Name")
    # Check if is_public param is valid.
    if not isinstance(is_public, bool):
        raise InputError(description="Invalid is_public variable")

    # Create and check that channel id is unique...
    channel_id = data.generate_channel_id()

    # Create channel data structure & add new information...
    data.data['channels'].append({
        'id': channel_id,
        'name' : name,
        'members': {
            'permission_id_1': [data.token_to_user_id(token)],
            'permission_id_2': [],
        },
        'messages': [],
        'is_public': is_public,
        'standup': {
            'creator': None,
            'time_finish': None,
            'messages': []
        },
        'is_censored': False
    })

    return {
        'channel_id': channel_id,
    }
