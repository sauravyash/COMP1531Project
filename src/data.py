# This file contains the appliation state data that is shared by the entire program
import re
import hashlib
import jwt

global data
data = {
    'users': [],
    'channels': []
}

JWT_KEY = 'b0ggers'

# returns user id of given user token
# Raises a LookupError if token is not found

def resolve_token(token):
    decoded_jwt = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
    for user in data['users']:
        if jwt.decode(user['token'], JWT_KEY, algorithms=['HS256']) == decoded_jwt and user['authenticated']:
            return user['id']

    raise LookupError("Token not found") # pragma: no cover

def resolve_user_id_index(user_id):
    for i, user in enumerate(data["users"]):
        if user['id'] == user_id:
            return i

    raise LookupError("user id not found")

def resolve_channel_id_index(channel_id):
    for i, channel in enumerate(data["channels"]):
        if channel['id'] == channel_id:
            return i

    raise LookupError("channel id not found")

def resolve_message_id_index(message_id):
    for channel in data["channels"]:
        for i, msg in enumerate(channel["messages"]):
            if msg['message_id'] == message_id:
                return (channel['id'], i)

    raise LookupError("message id not found")

def print_data():
    print(data)

#NOT MINE, from spec sheet
def check_email(email):
    """ Checks if email is valid

    Arguments: email, must be string
    Returns: True/False
    """
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    return bool(re.search(regex, email))

# Checks if input password is valid (i.e. has length more than 5 characters)
def check_password(password):
    """ Checks if password is valid

    Input arguments: password, must be string
    Returns: True/False
    """
    return len(password) >= 6

# Check is first and last names are between 1 and 50 characters inclusively
def check_name(name_first, name_last):
    """ Determines if names are valid, i.e. if name is between 1-50 characters

    Input arguments: name_first, name_last, must be strings
    Returns: True/False
    """
    return len(name_first) > 0 and len(name_first) < 51 and len(name_last) > 0 and len(name_last) < 51

# Loads all user_ids from database into id_list
def load_ids():
    """ Loads user_ids from data.py

    Returns: id_list
    """
    id_list = []
    for user in data["users"]:
        id_list.append(user["id"])

    return id_list

# Returns token index
def token_index(token):
    """ Looks up tokens to determine u_id index/token index

    Arguments: token, must be string
    Returns: Token index
    """
    for user in data["users"]: # pragma: no cover
        if jwt.decode(user['token'], JWT_KEY, algorithms=['HS256']) == jwt.decode(token, JWT_KEY, algorithms=['HS256']):
            return user["id"] - 1

    raise LookupError("Token not found") # pragma: no cover

# Determines if email has been registered
def search_emails(email):
    """ Searches through registered emails

    Arguments: email, must be string
    Returns: True/False
    """
    for user in data["users"]:
        if user["email"] == email:
            return True
    return False

# Returns user_id with respect to the email
def find_user_id_index(email):
    """ Looks up user id with respect to email

    Arguments: email, must be string
    Returns: user_id
    """
    for user in data["users"]: # pragma: no cover
        if user["email"] == email:
            return user["id"]

    raise LookupError("Email not found") # pragma: no cover

# Returns whether or not password matches respective email
def password_match(email, password):
    """ Compares password

    Arguments: email, password, must be strings
    Returns: True/False
    """
    return data["users"][find_user_id_index(email) - 1]["password"] == hashlib.sha256(password.encode()).hexdigest()

# Searches list of all stored handles and checks if handle has been found
def search_handle(handle):
    """ Searches through handles

    Arguments: handle, must be string
    Returns: True/False
    """
    for user in data["users"]:
        if user["handle"] == handle:
            return True
    return False

def generate_handle(handle):
    """ Generates unique handle

    Arguments: handle, must be string
    Returns: handle
    """
    while search_handle(handle):
        nums = []
        for i in range(len(handle)):
            if handle[i].isdigit():
                nums.append(handle[i])
        if nums == []:
            user_num = 1
        else:
            handle = handle[:len(handle) - len(nums)]
            user_num = int("".join(nums)) + 1

        handle += str(user_num)

        if len(handle) > 20: # pragma: no cover
            handle = handle[:20 - len(str(user_num))]
            handle += str(user_num)

    return handle

def search_msg_id(msg_id):
    try:
        channel_id, msg_index = resolve_message_id_index(msg_id)
        return {'channel': channel_id, 'msg_index': msg_index}
    except:
        return None


def generate_msg_id():
    generated_id = 0

    while True:
        if search_msg_id(generated_id) is None:
            yield generated_id
        generated_id += 1

def is_user_authorised(channel_id, user_id):
    try:
        channel_index = resolve_channel_id_index(channel_id)
        is_member = user_id in data.get('channels')[channel_index]['members']
        is_admin = user_id in data.get('channels')[channel_index]['admins']
        return is_admin or is_member
    except LookupError: # pragma: no cover
        return False

'''
EXAMPLE
data = {
    'users': [
        {
            'id': 1,
            'name_first': 'firstname',
            'name_last': 'lastname',
            'email': 'validemail@gmail.com',
            'password': 'validpassword123',
            'handle': 'firstnamelastname',
            'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6InRva2VuIn0.x8h0L 57fWirONi_9_ydVAcP41ObMCkf9HRsr2qJd00',
            'authenticated': True,
            'owner': 'user'
        },
        {
            'id': 2,
            'name' : 'user2',
            ...
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
    ]
}
'''
