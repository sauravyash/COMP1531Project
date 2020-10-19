import data
from error import InputError

def user_profile(token, u_id):

    try:
        u_id_index = data.resolve_user_id_index(u_id)
    except LookupError:
        raise InputError("User id not found")

    user_details = data.data["user"][u_id_index]

    return {
        'user': {
        	'u_id': user_details["u_id"],
        	'email': user_details["email"],
        	'name_first': user_details["name_first"],
        	'name_last': user_details["name_last"],
        	'handle_str': user_details["handle"],
        },
    }

def user_profile_setname(token, name_first, name_last):
    return {
    }

def user_profile_setemail(token, email):
    return {
    }

def user_profile_sethandle(token, handle_str):
    return {
    }
