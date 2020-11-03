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
    except LookupError: # pragma: no cover
        raise AccessError("Token not found")
    except:
        raise AccessError("Token not found")

    try:
        u_id_index = data.resolve_user_id_index(u_id)
    except LookupError:
        raise InputError("User id not found")

    user_details = data.data["users"][u_id_index]

    return {
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
    except LookupError:
        raise AccessError("Token not found")

    user_index = data.resolve_user_id_index(u_id)

    if not data.check_name(name_first, name_last):
        raise InputError

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
    except LookupError:
        raise AccessError("Token not found")

    user_index = data.resolve_user_id_index(u_id)

    if not data.check_email(email):
        raise InputError
    elif data.resolve_email(email):
        raise InputError

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
    except LookupError:
        raise AccessError("Token not found")

    user_index = data.resolve_user_id_index(u_id)

    if data.resolve_handle(handle_str):
        raise InputError
    elif len(handle_str) < 3:
        raise InputError
    elif len(handle_str) > 20:
        raise InputError

    data.data["users"][user_index]["handle"] = handle_str

    return {
    }

def user_profile_uploadphoto(token, url, x_start, y_start, x_end, y_end):
    ''' user can uploadphoto'''
    pass