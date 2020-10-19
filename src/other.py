import data
from error import AccessError
# Clears original data structure...
def clear():
    data.data = {
        'users': [],
        'channels': []
    }
    pass

def users_all(token):
    ''' Displays list of all users and respective data

    Arguments: token, must be string
    Returns: list of users
    '''
    try:
        data.resolve_token(token)
    except LookupError:
        raise AccessError("Token not found")

    return {
        data.data["users"]
    }
#    return {
#        'users': [
#            {
#                'u_id': 1,
#                'email': 'cs1531@cse.unsw.edu.au',
#                'name_first': 'Hayden',
#                'name_last': 'Jacobs',
#                'handle_str': 'hjacobs',
#            },
#        ],
#    }

def admin_userpermission_change(token, u_id, permission_id):
    pass

def search(token, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }
