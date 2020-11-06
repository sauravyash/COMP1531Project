''' Data.py
This file contains the application state data that is shared throughout the
entire program.

'''

import re
import hashlib
import jwt
import random
import string

global data
data = {
    'users': [],
    'channels': []
}

JWT_KEY = 'b0ggers'
EMAIL_PASSWORD = "comp1531admin"
EMAIL = "comp1531wed13grape3noreply@gmail.com"

#### ---- ALL FUNCTIONS THAT ACCESS AN ELEMENT IN THE DATA DICTIONARY ---- ####
# (Raises a LookupError if the element is not found.)

# TOKENS:
def token_to_user_id(token):
    """ FIND CORRESPONDING USER ID TO TOKEN
    Looks up tokens to determine corresponding user ID.

    Arguments: token- must be string
    Returns: Token index

    """
    token = token.encode('UTF-8')
    decoded_jwt = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
    for user in data['users']: # pragma: no cover
        if jwt.decode(user['token'], JWT_KEY, algorithms=['HS256']) == decoded_jwt and user['authenticated']:
            return user['id']

    raise LookupError("Token not found") # pragma: no cover

def resolve_token_index(token):
    """ FIND INDEX FOR TOKEN WITHIN DICTIONARY
    Looks up tokens to determine token index.

    Arguments: token- must be string
    Returns: Token index

    """
    token = token.encode('UTF-8')
    decoded_jwt = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
    for user in data["users"]:
        if jwt.decode(user['token'], JWT_KEY, algorithms=['HS256']) == decoded_jwt: # pragma: no cover
            return user["id"] - 1

    raise LookupError("Token not found") # pragma: no cover

# User ID
def resolve_user_id_index(user_id):
    """ FIND INDEX FOR USER ID WITHIN DICTIONARY
    Looks up user IDs to determine user ID index.

    Arguments: user id- must be an int
    Returns: User index

    """
    for i, user in enumerate(data["users"]):
        if user['id'] == user_id:
            return i

    raise LookupError("user id not found")

# Channel ID
def resolve_channel_id_index(channel_id):
    """ FIND INDEX FOR CHANNEL ID WITHIN DICTIONARY
    Looks up channel IDs to determine channel ID index.

    Arguments: channel id- must be an int
    Returns: Channel index

    """

    for i, channel in enumerate(data["channels"]):
        if channel['id'] == channel_id:
            return i

    raise LookupError("channel id not found")

# MESSAGE
def resolve_message_id_index(message_id):
    """ FIND INDEX FOR MESSAGE ID WITHIN DICTIONARY
    Looks up message IDs to determine message ID index.

    Arguments: message id- must be an int
    Returns: Message index

    """
    for channel in data["channels"]:
        for i, msg in enumerate(channel["messages"]):
            if msg['message_id'] == message_id:
                return (channel['id'], i)

    raise LookupError("message id not found")

def resolve_message_id(msg_id):
    ''' CHECK IF MESSAGE ID EXISTS WITHIN DICTIONARY

    Arguments: msg_id- must be an int
    Result: Either dictionary of channel_id and msg_index, or None

    '''
    try:
        channel_id, msg_index = resolve_message_id_index(msg_id)
        return {'channel_id': channel_id, 'msg_index': msg_index}
    except LookupError:
        return None

# EMAIL
def resolve_email(email):
    """ CHECK IF EMAIL HAS BEEN REGISTERED
    Searches through registered emails in dictionary.

    Arguments: email, must be string
    Returns: True/False

    """
    for user in data["users"]:
        if user["email"] == email:
            return True
    return False

def email_to_user_id(email):
    """ FIND CORRESPONDING USER ID TO EMAIL
    Looks up email to find corresponding user ID.

    Arguments: email, must be string
    Returns: user_id

    """
    for user in data["users"]: # pragma: no cover
        if user["email"] == email:
            return user["id"]

    raise LookupError("Email not found") # pragma: no cover

# USER PERMISSIONS
def resolve_permissions(channel_id, user_id):
    """ CHECK IF USER IS A MEMBER OF A CHANNEL & THEIR PERMISSIONS

    Arguments: channel_id- must be an int, user_id- must be an int
    Returns: Either 1 or 2- to indicate permissions; otherwise None

    """

    try:
        # Check if the user is a flockr owner.
        user_index = resolve_user_id_index(user_id)
        permission = data['users'][user_index]['permission_id']

        channel_index = resolve_channel_id_index(channel_id)
        members = data['channels'][channel_index]['members']

        # If user is a CHANNEL owner or FLOCKR owner, return 1.
        if user_id in members['permission_id_1']:
            return 1
        elif user_id in members['permission_id_2'] and permission == 1:
            return 1
        elif user_id in members['permission_id_2']:
            return 2
        else:
            return None
    except LookupError as e: # pragma: no cover
        raise e
        return None

# FOR TROUBLESHOOTING- PRINT THE CURRENT STATE OF THE DICTIONARY.
def print_data():
    print(data)

#### ---- ALL FUNCTIONS THAT AUTHENTICATE INPUT (FOR AUTH FUNCTIONS) ---- ####

#NOT MINE, from spec sheet.
def check_email(email):
    """ CHECK IF EMAIL IS VALID

    Arguments: email, must be string
    Returns: True/False

    """
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    return bool(re.search(regex, email))

def check_password(password):
    """ CHECK IF PASSWORD IS VALID
    Checks if input password is valid (i.e. has length more than 5 characters).

    Input arguments: password, must be string
    Returns: True/False

    """
    return len(password) >= 6

def check_name(name_first, name_last):
    """ CHECK IF NAME IS VALID
    Determines if names are valid, i.e. if name is between 1-50 characters.

    Input arguments: name_first, name_last, must be strings
    Returns: True/False

    """
    return len(name_first) > 0 and len(name_first) < 51 and len(name_last) > 0 and len(name_last) < 51

def all_users():
    """ CREATES A LIST OF ALL USERS WITHIN DICTIONARY
    Loads user IDs from data.py

    Returns: id_list

    """
    id_list = []
    for user in data["users"]:
        id_list.append(user["id"])

    return id_list

def password_match(email, password):
    """ CHECK IF PASSWORD MATCHES EMAIL
    Compares password to that stored in the dictionary with email.

    Arguments: email, password, must be strings
    Returns: True/False

    """
    return data["users"][email_to_user_id(email) - 1]["password"] == hashlib.sha256(password.encode()).hexdigest()

def reset_key_match(reset_key):
    """ CHECKS IF RESET KEY MATCHES
    Compares reset_key to reset the users password if it matches

    Arguments: reset_key, must be string
    Returns: True/False

    """
    for user in data["users"]:
        if user.get("reset_code") == hashlib.sha256(reset_key.encode()).hexdigest():
            user.pop("reset_code", None)
            return user.get("id")
    return 0

def resolve_handle(handle):
    """ CHECK IF HANDLE EXISTS WITHIN DICTIONARY
    Searches list of all stored handles and checks if handle exists.

    Arguments: handle, must be string
    Returns: True/False

    """
    for user in data["users"]:
        if user["handle"] == handle:
            return True
    return False

######## ----- ALL FUNCTIONS THAT GENERATE UNIQUE IDs OR HANDLES ----- ########

def generate_handle(handle):
    """ GENERATE UNIQUE HANDLE

    Arguments: handle- must be string
    Returns: Handle

    """
    while resolve_handle(handle):
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

def generate_message_id():
    """ GENERATE UNIQUE MESSAGE ID

    Arguments: msg_id- must be an int
    Returns: ID

    """
    generated_id = 0
    while resolve_message_id(generated_id):
        generated_id += 1
    return generated_id

def generate_channel_id():
    """ GENERATE UNIQUE CHANNEL ID

    Arguments: channel_id- must be an int
    Returns: ID

    """
    generated_id = 0
    while True:
        try:
            resolve_channel_id_index(generated_id)
            generated_id += 1
        except LookupError:
            return generated_id

def generate_reset_key(length):
    """ GENERATE RANDOM PASSWORD RESET CODE

    Arguments: length- must be an integer
    Returns: key

    """
    alphabet = string.ascii_letters
    key = ''.join(random.choice(alphabet) for i in range(length))

    return key

'''
EXAMPLE
EXAMPLE
data = {
    'users': [
        {
            'id': 1,
            'name_first': 'firstname1',
            'name_last': 'lastname1',
            'email': 'validemail1@gmail.com',
            'password': 'validpassword123',
            'handle': 'firstnamelastnam1',
            'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6InRva2VuIn0.x8h0L 57fWirONi_9_ydVAcP41ObMCkf9HRsr2qJd00',
            'authorised': True,
            'permission_id': 1,
        },
        {
            'id': 2,
            'name_first': 'firstname2',
            'name_last': 'lastname2',
            'email': 'validemail2@gmail.com',
            'password': 'validpassword123',
            'handle': 'firstnamelastnam2',
            'token': 'lkJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6InRva2VuIn0.x8h0L 57fWirONi_9_ydVAcP41ObMCkf9HRsr2qJd00',
            'authorised': True
            'permission_id': 2,
        },
    ],
    'channels': [
        {
            'id': 1,
            'name' : 'channel1',
            'members': [
                'permission_id_1': [],
                'permission_id_2': [],
            ]
            'messages' [
                  {
                      'message_id': 1,
                      'u_id': "mbr1",
                      'message': "hi"
                      'time_created': 1582426789
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
