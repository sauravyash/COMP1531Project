import data

from error import AccessError
from error import InputError

def channel_invite(token, channel_id, user_id):
    ''' Channel_invite
    Add a user to a channel (public or private) when they are invited by a user
    who is ALREADY a MEMBER of that channel.
    
    Arguments: token- must be a valid int, channel_id- must be a valid int,
    user_id- must be a valid int
    Result: Empty dictionary {}
    
    '''
    
    # Find index of channel and check channel ID is valid.
    try:
        channel_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError(description='Invalid Channel ID')

    # Check that user ID is valid.
    try:
        data.resolve_user_id_index(user_id)
    except LookupError:
        raise InputError(description='Invalid User ID')
    
    # Check that the token is valid.
    try:
        user_id_token = data.token_to_user_id(token)
    except:
        raise AccessError(description='Invalid Token')

    # To cause less confusion, name accordingly.
    invited_member = user_id
    already_member = user_id_token
    
    # Check that the authorised user is already a member of the channel.
    channel = data.data['channels'][channel_index]
    if data.resolve_permissions(channel['id'], already_member) is None:
        raise AccessError(description='Authorised User Not Member of Channel')

    # Add the user to the list of permission id 2 members.
    channel['members']['permission_id_2'].append(invited_member)

    return {}

def channel_details(token, channel_id):
    ''' Channel_details
    Provide details about a channel a user is a member of.
    
    Input: token- must be a valid int, channel_id- must be a valid int
    Result: A dictionary containing a channel's name, owner_members and all 
    members (overlapping with owner_members)
    
    '''
    
    # Find index of channel and check channel ID is valid.
    try:
        channel_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError(description='Invalid Channel ID')
        
    # Check that the token is valid.
    try:
        user_id = data.token_to_user_id(token)
    except:
        raise AccessError(description='Invalid Token')

    # Check that the user is a member of the channel.
    channel = data.data['channels'][channel_index]
    members = channel['members']
    channel_members = members['permission_id_1'] + members['permission_id_2']
    if data.resolve_permissions(channel['id'], user_id) is None:
        raise AccessError(description='Authorised User Not Member of Channel')
    
    # Return channel details as a dictionary.
    return {
        'name': channel['name'],
        'owner_members': members['permission_id_1'],
        'all_members': channel_members,
    }


def channel_messages(token, channel_id, start):
    ''' Channel_messages
    Select the 50 most recent messages and display from a starting point.
    
    Input: token- must be a valid int, channel_id- must be a valid int, start-
    must be a valid int between 0 and number of messages.
    Result: A list of the 50 most recent messages; or if there are less than 50,
    of all messages in order from most to least recent.
    
    '''
    
    # Find index of channel and check channel ID is valid.
    try:
        channel_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError('Channel not found')
        
    # Check that the token is valid.
    try:
        user_id = data.token_to_user_id(token)
    except:
        raise AccessError(description='Invalid Token')
    
    # Check that the user is a member of the channel.
    channel = data.data['channels'][channel_index]
    if data.resolve_permissions(channel['id'], user_id) is None:
        raise AccessError(description='Authorised User Not Member of Channel')
        
    # Reverse messages list, so that most recent is index 0.
    messages = list(reversed(channel['messages']))
    # Check if start param is valid.
    if start > len(messages) or start < 0:
        raise InputError('Start is Out of Bounds')

    # Display up to 50 messages.
    end = start + 50 if len(messages) - start >= 50 else -1
    if len(messages) - start >= 50:
        returned_msgs = messages[start:end]
    else:
        returned_msgs = messages[start:] 
    
    return {
        'messages': returned_msgs,
        'start': start,
        'end': end,
    }

def channel_leave(token, channel_id):
    ''' Channel_leave
    Allow any member to leave any channel.
    
    Input: token- must be a valid int, channel_id- must be a valid int
    Result: Empty dictionary, {}
    
    '''
    
    # Find index of channel and check channel ID is valid.
    try:
        channel_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError(description='Invalid Channel ID')

    # Check that token is valid.
    try:
        user_id = data.token_to_user_id(token)
    except:
        raise AccessError(description='Invalid Token')

    # If the user is a member of the channel, then remove them.
    # Add a function that checks if the user is the only user, then delete the
    # channel.
    channel = data.data['channels'][channel_index]
    if data.resolve_permissions(channel['id'], user_id) is not None:
        if user_id in channel['members']['permission_id_1']:
            channel['members']['permission_id_1'].remove(user_id)
        else:
            channel['members']['permission_id_2'].remove(user_id)
    else:
        raise AccessError(description='Authorised User Not Member of Channel')

    return {}

def channel_join(token, channel_id):
    ''' Channel_join
    Allow any member to join a public channel or a flockr owner to join any
    channel.
    
    Input: token- must be a valid int, channel_id- must be a valid int
    Result: Empty dictionary, {}
    
    '''
    
    # Find index of channel and check channel ID is valid.
    try:
        channel_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError(description='Invalid Channel ID')

    # Check that token and user ID is valid.
    try:
        user_id = data.token_to_user_id(token)
        user_index = data.resolve_user_id_index(user_id)
    except:
        raise AccessError(description='Invalid Token')
    
    # If member is already in channel, do not add twice.
    channel = data.data['channels'][channel_index]
    if data.resolve_permissions(channel['id'], user_id) is not None:
        return {}
    
    # Check if member is a global owner (owner of flockr)
    global_permission = data.data['users'][user_index]['permission_id']
    
    # Add authorised user to the channel or raise error.
    if channel['is_public'] or global_permission == 1:
        channel['members']['permission_id_2'].append(user_id)
    else:
        raise AccessError(description='User Not Authorised to Access Channel')

    return {}

def channel_addowner(token, channel_id, user_id):

    # channel
    try:
        channe_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError('Invalid channel ID')

    # user
    try:
        data.resolve_user_id_index(user_id)
    except LookupError:
        raise InputError('Invalid user ID')

    # user id from token
    user = data.token_to_user_id(token)
    is_owner = data.data['users'][data.resolve_user_id_index(user)]['owner']
    if is_owner != 'owner':
        raise AccessError('Not an owner of the specified channel')

    # user id from parameter
    is_owner = data.data['users'][data.resolve_user_id_index(user_id)]['owner']
    if is_owner == 'owner':
        raise AccessError('Target user already an owner of the channel')

    data.data['channels'][channel_index]['admins'].append(user_id)

    return {
    }

def channel_removeowner(token, channel_id, user_id):

    # channel
    try:
        channel_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError('Invalid channel ID')

    # user
    try:
        data.resolve_user_id_index(user_id)
    except LookupError: # pragma: no cover
        raise InputError('Invalid user ID')

    # user id from parameter
    # remove a member that is not owner
    is_owner = data.data['users'][data.resolve_user_id_index(user_id)]['owner']
    if is_owner != 'owner':
        raise InputError('Target user already an owner of the channel')

    # user id from token
    # remove not from owner
    user = data.token_to_user_id(token)
    is_owner = data.data['users'][data.resolve_user_id_index(user)]['owner']
    if is_owner != 'owner':
        raise AccessError('Not an owner of the specified channel')


    data.data['channels'][channel_index]['admins'].remove(user_id)

    return {
    }
