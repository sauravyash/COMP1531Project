# This file contains the appliation state data that is shared by the entire program
global data
data = {
    'users': [],
    'channels': []
}

# returns user id of given user token
# Raises a LookupError if token is not found
def resolve_token(token):
    token_list = []
    for i in range(0, len(data.get("users"))):
        token_list.append(data.get("users")[i].get("token"))

    return token_list.index(token)

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



'''
EXAMPLE
data = {
    'users': [
        {
            'id': 1,
            'name' : 'user1',
        },
        {
            'id': 2,
            'name' : 'user2',
        },
    ],
    'channels': [
        {
            'id': 1,
            'name' : 'channel1',
            'admins': [ 'exampleID1', 'exampleID2'],
            'members': [ 'mbr1', 'mbr2'] ,
            'messages' [
                  {
                      'msg_id': 1,
                      'msg_author': "mbr1",
                      'msg_content': "hi"
                  }
             ]
            'is_public': True
        },
        {
            'id': 2,
            'name' : 'channel2',
            ...
        },
    ],
    'tokens': [
        {
            'user_id': "mbr1",
            'token': "1234"
        },
        {
            ...
        }
    ]
}
'''
