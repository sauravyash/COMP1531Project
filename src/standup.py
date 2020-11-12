''' Standup.py
File that contains all functions related to standup.

'''

import datetime
import data
import message

from error import InputError, AccessError

def standup_start(token, channel_id, length):

	# Check token is valid.
    try:
        data.token_to_user_id(token)
    except:
        raise AccessError(description='Invalid token')

    # Check channel ID is valid.
    try:
        channel_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError(description='Invalid Channel ID')


	# Check that there is not already an active standup in this channel.
    if standup_active(token, channel_id)['is_active'] is True:
        raise InputError(description='Standup Already Active')

    current_time = datetime.datetime.now()
    finish_time = current_time + datetime.timedelta(seconds=length)
    finish_time = finish_time.timestamp()

	# Edit data structure to store standup details.
    standup = data.data['channels'][channel_index]['standup']
    standup['time_finish'] = finish_time
    standup['messages'] = []
    standup['creator'] = token

    return  {'time_finish': finish_time}

# Close a standup and clear standup data.
def close_standup(channel_index, channel_id):
    # Collate all messages sent.
    standup = data.data['channels'][channel_index]['standup']

    standup_str = 'Standup Minutes: \n'

    for message_info in standup['messages']: # pragma: no cover
	    user_index = data.resolve_user_id_index(message_info['u_id'])
	    # Use handle rather than first name as handle is unique.
	    handle = data.data['users'][user_index]['handle']
	    # Add a message in format 'hayden: I ate a catfish'.
	    standup_str += handle + ': '+ message_info['message'] + '\n'

    # Send out collated messages (unless no messages were sent during standup).	
    try:
        send_time = standup['time_finish']
        message.message_sendlater(standup['creator'], channel_id, standup_str, send_time)
    except InputError:
        message.message_send(standup['creator'], channel_id, standup_str)

    # Clear data
    standup['time_finish'] = None
    standup['messages'] = []
    standup['creator'] = None

def standup_active(token, channel_id):

	# Check token is valid.
    try:
        data.token_to_user_id(token)
    except:
        raise AccessError(description="Invalid token")

    # Check channel ID is valid.
    try:
        channel_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError(description='Invalid Channel ID')

    current_time = datetime.datetime.now().timestamp()

    active = False

    standup = data.data['channels'][channel_index]['standup']
    # Check if any data for a standup has been stored
    if standup['time_finish'] is not None:
	    if standup['time_finish'] <= current_time:
		    # Close the standup:
		    # ie. send out final message and erase all data.
		    close_standup(channel_index, channel_id)
	    else:
		    active = True

    return {
	    'is_active': active,
        'time_finish':  standup['time_finish']
        }

def standup_send(token, channel_id, message):

    # Check token is valid.
    try:
        u_id = data.token_to_user_id(token)
    except:
        raise AccessError(description="Invalid token")

    # Check channel ID is valid.
    try:
        channel_index = data.resolve_channel_id_index(channel_id)
    except LookupError:
        raise InputError(description='Invalid Channel ID')

    # Check that message is valid.
    if len(message) > 1000:
	    raise InputError(description='Message Too Long')

    # Check that standup is active in this channel.
    if standup_active(token, channel_id)['is_active'] is False:
	    raise InputError(description='Standup Not Active')

    # Check that user is authorised to send a message in channel.
    permissions = [1, 2]
    if data.resolve_permissions(channel_id, u_id) not in permissions:
	    raise AccessError(description='User Not Authorised')

    # Store the message in standup buffer.
    standup = data.data['channels'][channel_index]['standup']
    standup['messages'].append({
	    'u_id': u_id,
	    'message': message
	    })

    return {}
