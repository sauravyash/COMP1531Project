# This file contains the appliation state data that is shared by the entire program
global data
data = {
    'users': [],
    'channels': []
}

# returns user id of given user token
# Raises a LookupError if token is not found

def resolve_token(token):
    for user in data['users']:
        if user['token'] == token and user['authenticated']:
            return user['id']

    raise LookupError("Token not found")

def resolve_user_id_index(user_id):
    i = 0
    for user in data["users"]:
        if user['id'] == user_id:
            return i
        else:
            i += 1
    raise LookupError("user_id not found")

def resolve_channel_id_index(channel_id):
    i = 0
    for channel in data["channels"]:
        if channel['id'] == channel_id:
            return i
        else:
            i += 1
    raise LookupError("channel_id not found")

def resolve_message_id_index(channel_id, user_id):
    pass

def print_data():
    print(data)



