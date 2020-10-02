import re
import data
from error import InputError

#NOT MINE, from spec sheet
def check_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' #NOT MINE, from spec sheet
    if (re.search(regex, email)):
        return True
    else:
        return False

# Checks if input password is valid (i.e. has length more than 5 characters)
def check_password(password):
    if (len(password) < 6):
        return False
    return True

# Check is first and last names are between 1 and 50 characters inclusively
def check_name(name_first, name_last):
    if (len(name_first) > 0 and len(name_first) < 51 and len(name_last) > 0 and len(name_last) < 51):
        return True
    return False

# Loads all emails from database into emails_list
def load_emails():
    email_list = []
    for i in range(0, len(data.data.get("users"))):
        email_list.append(data.data.get("users")[i].get("email"))

    return email_list

# Loads all user_ids from database into id_list
def load_ids():
    id_list = []
    for i in range(0, len(data.data.get("users"))):
        id_list.append(data.data.get("users")[i].get("id"))

    return id_list

def token_index(token):
    token_list = []
    for i in range(0, len(data.data.get("users"))):
    #    email_list.append(data.data.get("users")[i].get("email"))
        token_list.append(data.data.get("users")[i].get("token"))

    return token_list.index(token)

# Searches list of all stored emails and checks if email has been found
def search_emails(email):
    #email_list = []
    #for i in range(0, len(data.data.get("users"))):
    #    email_list.append(data.data.get("users")[i].get("email"))

    if email in load_emails():
        return True
    return False

# Returns user_id with respect to the email (false if not found)
def search_u_id(email):
    #email_list = []
    id_list = []
    for i in range(0, len(data.data.get("users"))):
    #    email_list.append(data.data.get("users")[i].get("email"))
        id_list.append(data.data.get("users")[i].get("id"))

    return id_list[load_emails().index(email)]

# Returns password with respect to the email (false if not found)
def search_passwords(email, password):
    #email_list = []
    password_list = []
    for i in range(0, len(data.data.get("users"))):
    #    email_list.append(data.data.get("users")[i].get("email"))
        password_list.append(data.data.get("users")[i].get("password"))

    if password_list[load_emails().index(email)] == password:
        return True
    return False

def load_tokens(token):
    token_list = []
    for i in range(0, len(data.data.get("users"))):
    #    email_list.append(data.data.get("users")[i].get("email"))
        token_list.append(data.data.get("users")[i].get("token"))

# Searches list of all stored handles and checks if handle has been found
def search_handle(handle):
    handle = []
    for i in range(0, len(data.data.get("users"))):
        handle_list.append(data.data.get("users")[i].get("handle"))

    if handle in handle_list:
        return True
    return False









def auth_login(email, password):
    if (check_email(email) == False):
        raise InputError
        #print("CHECK EMAIL")
        return {
            'u_id': 0,
            'token': email + "invalid",
        }
    elif (search_emails(email) == False):
        raise InputError
        #print("SEARCH EMAIL")
        return {
            'u_id': 0,
            'token': email + "invalid",
        }
    elif (search_passwords(email, password) == False):
        raise InputError
        #print("CHECK PASSWORD")
        return {
            'u_id': 0,
            'token': email + "invalid",
        }

    return {
        'u_id': search_u_id(email),
        'token': email,
    }

def auth_logout(token):
    #tokens appened with "invalid" are not authenticated
    if token[-7:] == "invalid":
        return {
            'is_success': False,
        }
    else:
        #deauthenticate token (token = token + "invalid")
        data.data["users"][token_index(token)]["token"] = token + "invalid"

        return {
            'is_success': True,
        }

def auth_register(email, password, name_first, name_last):
    #ASSUMPTION: User_id = 0 means error
    #check if email not already being used
    #check if email if valid
    #check if password is valid
    #check if name is valid

    #if all true generate new user_id (increment from last user_id in database)
    #generate handle, generate token (email for now), store password and names

    #retrieve list of all users and search to see if email is there


    if (check_email(email) == False):
        raise InputError
        return {
            'u_id': 0,
            'token': email + "invalid",
        }
    elif (search_emails(email)):
        raise InputError
        return {
            'u_id': 0,
            'token': email + "invalid",
        }
    elif (check_password(password) == False):
        raise InputError
        return {
            'u_id': 0,
            'token': email + "invalid",
        }
    elif (check_name(name_first, name_last) == False):
        raise InputError
        return {
            'u_id': 0,
            'token': email + "invalid",
        }

    handle = name_first.lower() + name_last.lower()
    if (len(handle) > 20):
        handle = handle[:20]


    #if (search_handle(handle)): append a number
        #modify handle


    #store password, handle, names
    #generate user id by incrementing largest user_id in database
    #store email, user_id

    new_id = max(load_ids()) + 1

    data.data.get("users").append({'id': new_id, 'name_first': name_first, 'name_last': name_last, 'email': email, 'password': password, 'handle': handle, 'token': email})

    return {
        'u_id': new_id, #next user_id
        'token': email,
    }
