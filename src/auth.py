""" Authentication functions

"""
import re
import data
import hashlib
import jwt
from error import InputError

def auth_login(email, password):
    """ Logs in the user, authenticating their token

    Arguments: email, password, must be string
    Returns u_id, token
    """
    if not data.check_email(email):
        raise InputError
    elif not data.resolve_email(email):
        raise InputError
    elif not data.password_match(email, password):
        raise InputError

    data.data["users"][data.email_to_user_id(email) - 1]["authenticated"] = True

    return {
        'u_id': data.email_to_user_id(email),
        'token': jwt.encode({"u_id": data.email_to_user_id(email)}, data.JWT_KEY, algorithm='HS256'),
    }

def auth_logout(token):
    """ Logs out the user, deathenticating their token

    Arguments: token, must be string
    Returns: is_success
    """
    if not data.data["users"][data.resolve_token_index(token)]["authenticated"]:
        return {
            'is_success': False,
        }
    #deauthenticate token
    data.data["users"][data.resolve_token_index(token)]["authenticated"] = False

    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):
    """ Registers a new user, adding their details to the database

    Arguments: email, password, name_first, name_last, must be strings
    Returns: u_id, token
    """
    user_one = 0
    if data.data["users"] == []:
        user_one = 1

    if not data.check_email(email):
        raise InputError
    elif data.resolve_email(email) and user_one == 0:
        raise InputError
    elif not data.check_password(password):
        raise InputError
    elif not data.check_name(name_first, name_last):
        raise InputError

    handle = name_first.lower() + name_last.lower()

    if len(handle) > 20: # pragma: no cover
        handle = handle[:20]

    handle = data.generate_handle(handle)

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
            'password': hashlib.sha256(password.encode()).hexdigest(),
            'handle': handle,
            'token': jwt.encode({"u_id": new_id}, data.JWT_KEY, algorithm='HS256'),
            'authenticated': True,
            'permission_id': 1,
        })
    else:
        new_id = max(data.all_users()) + 1
        data.data.get("users").append({
            'id': new_id,
            'name_first': name_first,
            'name_last': name_last,
            'email': email,
            'password': hashlib.sha256(password.encode()).hexdigest(),
            'handle': handle,
            'token': jwt.encode({"u_id": new_id}, data.JWT_KEY, algorithm='HS256'),
            'authenticated': True,
            'permission_id': 2,
        })

    return {
        'u_id': new_id, #next user_id
        'token': jwt.encode({"u_id": new_id}, data.JWT_KEY, algorithm='HS256'),
    }
