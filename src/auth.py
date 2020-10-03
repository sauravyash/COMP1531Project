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

    #return re.search(regex, email)

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
    for user in data.data["users"]:
        email_list.append(user["email"])

    return email_list

# Loads all user_ids from database into id_list
def load_ids():
    id_list = []
    for user in data.data["users"]:
        id_list.append(user["id"])

    return id_list

def load_tokens():
    token_list = []
    for user in data.data["users"]:
        token_list.append(user["token"])

    return token_list

def token_index(token):
    token_list = load_tokens()

    return token_list.index(token)

# Searches list of all stored emails and checks if email has been found
def search_emails(email):
    if email in load_emails():
        return True
    return False

# Returns user_id with respect to the email (false if not found)
def search_u_id(email):
    id_list = load_ids()

    return id_list[load_emails().index(email)]

# Returns password with respect to the email (false if not found)
def search_passwords(email, password):
    password_list = []
    for user in data.data["users"]:
        password_list.append(user["password"])

    if password_list[load_emails().index(email)] == password:
        return True
    return False



# Searches list of all stored handles and checks if handle has been found
def search_handle(handle):
    handle_list = []
    for user in data.data["users"]:
        handle_list.append(user["handle"])

    if handle in handle_list:
        return True
    return False









def auth_login(email, password):
    if (check_email(email) == False):
        raise InputError
        return {
            'u_id': 0,
            'token': email,
        }
    elif (search_emails(email) == False):
        raise InputError
        return {
            'u_id': 0,
            'token': email,
        }
    elif (search_passwords(email, password) == False):
        raise InputError
        return {
            'u_id': 0,
            'token': email,
        }

    data.data["users"][load_emails().index(email)]["authenticated"] = True

    return {
        'u_id': search_u_id(email),
        'token': email,
    }

def auth_logout(token):
    #tokens appened with "invalid" are not authenticated
    if data.data["users"][token_index(token)]["authenticated"] == False:
        return {
            'is_success': False,
        }
    else:
        #deauthenticate token (token = token + "invalid")
        data.data["users"][token_index(token)]["authenticated"] = False

        return {
            'is_success': True,
        }

def auth_register(email, password, name_first, name_last):
    user_one = 0
    if data.data["users"] == []:
        user_one = 1

    if (check_email(email) == False):
        raise InputError
        return {
            'u_id': 0,
            'token': email,
        }
    elif (search_emails(email) and user_one == 0):
        raise InputError
        return {
            'u_id': 0,
            'token': email,
        }
    elif (check_password(password) == False):
        raise InputError
        return {
            'u_id': 0,
            'token': email,
        }
    elif (check_name(name_first, name_last) == False):
        raise InputError
        return {
            'u_id': 0,
            'token': email,
        }

    handle = name_first.lower() + name_last.lower()
    if (len(handle) > 20):
        handle = handle[:20]

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
            handle += str(handle)

    #store password, handle, names
    #generate user id by incrementing largest user_id in database
    #store email, user_id

    if (user_one): #generate first user
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
