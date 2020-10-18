""" Authentication functions

"""
import re
import data
from error import InputError

#NOT MINE, from spec sheet
def check_email(email):
    """ Checks if email is valid

    Arguments: email, must be string
    Returns: True/False
    """
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if re.search(regex, email):
        return True
    return False

# Checks if input password is valid (i.e. has length more than 5 characters)
def check_password(password):
    """ Checks if password is valid

    Input arguments: password, must be string
    Returns: True/False
    """
    if len(password) < 6:
        return False
    return True

# Check is first and last names are between 1 and 50 characters inclusively
def check_name(name_first, name_last):
    """ Determines if names are valid

    Input arguments: name_first, name_last, must be strings
    Returns: True/False
    """
    if (len(name_first) > 0 and len(name_first) < 51 and len(name_last) > 0 and len(name_last) < 51):
        return True
    return False

# Loads all user_ids from database into id_list
def load_ids():
    """ Loads user_ids from data.py

    Returns: id_list
    """
    id_list = []
    for user in data.data["users"]:
        id_list.append(user["id"])

    return id_list

# Returns token index
def token_index(token):
    """ Looks up tokens

    Arguments: token, must be string
    Returns: Token index
    """
    for user in data.data["users"]:
        if user["token"] == token:
            return user["id"] - 1

    raise LookupError("Token not found")

# Determines if email has been registered
def search_emails(email):
    """ Searches through registered emails

    Arguments: email, must be string
    Returns: True/False
    """
    for user in data.data["users"]:
        if user["email"] == email:
            return True
    return False

# Returns user_id with respect to the email
def u_id_index(email):
    """ Looks up user id with respect to email

    Arguments: email, must be string
    Returns: user_id
    """
    for user in data.data["users"]:
        if user["email"] == email:
            return user["id"]

    raise LookupError("Email not found")

# Returns whether or not password matches respective email
def password_match(email, password):
    """ Compares password

    Arguments: email, password, must be strings
    Returns: True/False
    """
    if data.data["users"][u_id_index(email) - 1]["password"] == password:
        return True
    return False

# Searches list of all stored handles and checks if handle has been found
def search_handle(handle):
    """ Searches through handles

    Arguments: handle, must be string
    Returns: True/False
    """
    for user in data.data["users"]:
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

        if len(handle) > 20:
            handle = handle[:20 - len(str(user_num))]
            handle += str(user_num)

    return handle

def auth_login(email, password):
    """ Logs in the user

    Arguments: email, password, must be string
    Returns u_id, token
    """
    if not check_email(email):
        raise InputError
    elif not search_emails(email):
        raise InputError
    elif not password_match(email, password):
        raise InputError

    data.data["users"][u_id_index(email) - 1]["authenticated"] = True

    return {
        'u_id': u_id_index(email),
        'token': email,
    }

def auth_logout(token):
    """ Logs out the user

    Arguments: token, must be string
    Returns: is_success
    """
    if not data.data["users"][token_index(token)]["authenticated"]:
        return {
            'is_success': False,
        }
    #deauthenticate token
    data.data["users"][token_index(token)]["authenticated"] = False

    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):
    """ Registers a new user

    Arguments: email, password, name_first, name_last, must be strings
    Returns: u_id, token
    """
    user_one = 0
    if data.data["users"] == []:
        user_one = 1

    if not check_email(email):
        raise InputError
    elif search_emails(email) and user_one == 0:
        raise InputError
    elif not check_password(password):
        raise InputError
    elif not check_name(name_first, name_last):
        raise InputError

    handle = name_first.lower() + name_last.lower()

    if len(handle) > 20:
        handle = handle[:20]

    handle = generate_handle(handle)

    #store password, handle, names
    #generate user id by incrementing largest user_id in database
    #store email, user_id

    if user_one: #generate first user
        new_id = 1
        data.data.get("users").append({
            'id': new_id,
            'name_first': name_first,
            'name_last': name_last,
            'email': email,
            'password': password,
            'handle': handle,
            'token': email,
            'authenticated': True,
            'owner': "owner"
        })
    else:
        new_id = max(load_ids()) + 1
        data.data.get("users").append({
            'id': new_id,
            'name_first': name_first,
            'name_last': name_last,
            'email': email,
            'password': password,
            'handle': handle,
            'token': email,
            'authenticated': True,
            'owner': "user"
        })

    return {
        'u_id': new_id, #next user_id
        'token': email,
    }
