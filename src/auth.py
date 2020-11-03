""" Authentication functions
This file contains all function to do with the authentication and setup of a
flockr user.
"""

import hashlib
import smtplib
import ssl
import jwt
import data
from error import InputError, AccessError

def auth_login(email, password):
    """ Logs in the user, authenticating their token

    Arguments: email, password, must be string
    Returns u_id, token
    """
    # Check that the email is valid and matches a password.
    if not data.check_email(email):
        raise InputError
    elif not data.resolve_email(email):
        raise InputError
    elif not data.password_match(email, password):
        raise InputError

    # Autheticate the user (as being logged in)
    data.data["users"][data.email_to_user_id(email) - 1]["authenticated"] = True

    return {
        'u_id': data.email_to_user_id(email),
        'token': jwt.encode({"u_id": data.email_to_user_id(email)}, data.JWT_KEY, algorithm='HS256').decode('UTF-8')
    }

def auth_logout(token):
    """ Logs out the user, deathenticating their token

    Arguments: token, must be string
    Returns: is_success
    """
    # Check that token exists.
    try:
        data.resolve_token_index(token)
    except:
        raise AccessError

    if not data.data["users"][data.resolve_token_index(token)]["authenticated"]:
        return {
            'is_success': False,
        }
    # Deauthenticate token for log out.
    data.data["users"][data.resolve_token_index(token)]["authenticated"] = False

    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):
    """ Registers a new user, adding their details to the database

    Arguments: email, password, name_first, name_last, must be strings
    Returns: u_id, token
    """
    # Register the first user.
    user_one = 0
    if data.data["users"] == []:
        user_one = 1

    # Check that the email, password and names are valid input.
    if not data.check_email(email):
        raise InputError
    elif data.resolve_email(email) and user_one == 0:
        raise InputError
    elif not data.check_password(password):
        raise InputError
    elif not data.check_name(name_first, name_last):
        raise InputError

    # Create a handle.
    handle = name_first.lower() + name_last.lower()

    if len(handle) > 20: # pragma: no cover
        handle = handle[:20]

    handle = data.generate_handle(handle)

    # store password, handle, names
    # generate user id by incrementing largest user_id in database
    # store email, user_id

    if user_one: # generate first user. (flockr owner)
        new_id = 1
        permission = 1
    else: # generate any other user.
        new_id = max(data.all_users()) + 1
        permission = 2

    data.data.get("users").append({
        'id': new_id,
        'name_first': name_first,
        'name_last': name_last,
        'email': email,
        'password': hashlib.sha256(password.encode()).hexdigest(),
        'handle': handle,
        'token': jwt.encode({"u_id": new_id}, data.JWT_KEY, algorithm='HS256'),
        'authenticated': True,
        'permission_id': permission,
    })


    encoded_jwt = jwt.encode({"u_id": new_id}, data.JWT_KEY, algorithm='HS256')
    decoded_string = encoded_jwt.decode('UTF-8')

    return {
        'u_id': new_id, #next user_id
        'token': decoded_string
    }

def auth_passwordreset_request(email):
    """ Sends reset_key to user's email

    Arguments: email- must be string
    Returns: empty dictionary
    """
    try:
        u_id_index = data.email_to_user_id(email) - 1
    except:
        raise InputError

    reset_key = data.generate_reset_key(8)

    data.data["users"][u_id_index]["reset_code"] = hashlib.sha256(reset_key.encode()).hexdigest()

    # Send user email containing reset_code
    # from https://realpython.com/python-send-email/

    port = 465
    smtp_server = "smtp.gmail.com"
    receiver_email = email
    #message = """\
    #Subject: flockr password reset request

    #Your reset code is: """ + str(reset_key)
    SUBJECT = "flockr password reset request"
    TEXT = "Your reset code is: " + str(reset_key)

    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(data.EMAIL, data.EMAIL_PASSWORD)
        server.sendmail(data.EMAIL, receiver_email, message)
        server.quit()

    return {}

def auth_passwordreset_reset(reset_code, new_password):
    """ Resets the user's password

    Arguments: reset_code, new_password- must be strings
    Returns: empty dictionary
    """

    u_id = data.reset_key_match(reset_code)

    if u_id == 0:
        raise InputError
    elif not data.check_password(new_password):
        raise InputError

    data.data["users"][u_id - 1]["password"] = hashlib.sha256(new_password.encode()).hexdigest()

    return {}
