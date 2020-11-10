''' user functions
'''
import data
from error import InputError
from error import AccessError

def user_profile(token, u_id):
    ''' Display user's profile data

    Arguments: token, u_id, token is is string, u_id is integer
    Returns: user
    '''
    try:
        data.token_to_user_id(token)
    except:
        raise AccessError(description="Token not found")

    try:
        u_id_index = data.resolve_user_id_index(u_id)
    except LookupError:
        raise InputError(description="User id not found")

    user_details = data.data["users"][u_id_index] # pragma: no cover

    return { # pragma: no cover
        'user': {
    	'u_id': user_details["id"],
    	'email': user_details["email"],
    	'name_first': user_details["name_first"],
    	'name_last': user_details["name_last"],
    	'handle_str': user_details["handle"],
        },
    }

def user_profile_setname(token, name_first, name_last):
    ''' Changes user's current first name and last name

    Arguments: token, name_first, name_last, must be strings
    Returns: empty dictionary
    '''
    try:
        u_id = data.token_to_user_id(token)
    except: # pragma: no cover
        raise AccessError(description="Token not found")

    user_index = data.resolve_user_id_index(u_id)

    if not data.check_name(name_first, name_last):
        raise InputError(description="Invalid first name or last name")

    # storing user's new first and last names
    data.data["users"][user_index]["name_first"] = name_first
    data.data["users"][user_index]["name_last"] = name_last

    return {
    }

def user_profile_setemail(token, email):
    ''' Changes user's current email

    Arguments: token, email, must be strings
    Return: empty dictionary
    '''
    try:
        u_id = data.token_to_user_id(token)
    except: # pragma: no cover
        raise AccessError(description="Token not found")

    user_index = data.resolve_user_id_index(u_id)

    if not data.check_email(email):
        raise InputError(description="Invalid email")
    elif data.resolve_email(email):
        raise InputError(description="Email not found")

    # storing user's new email address
    data.data["users"][user_index]["email"] = email

    return {
    }

def user_profile_sethandle(token, handle_str):
    ''' Changes user's current handle

    Arguments: token, handle_str, must be string
    Returns: empty dictionary
    '''
    try:
        u_id = data.token_to_user_id(token)
    except: # pragma: no cover
        raise AccessError(description="Token not found")

    user_index = data.resolve_user_id_index(u_id)

    if data.resolve_handle(handle_str):
        raise InputError(description="Handle already in user")
    elif len(handle_str) < 3:
        raise InputError(description="Handle too short")
    elif len(handle_str) > 20:
        raise InputError(description="Hanle too long")

    # storing user's new handle
    data.data["users"][user_index]["handle"] = handle_str

    return {
    }
