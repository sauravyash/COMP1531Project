import sys
import os
import json
from json import dumps
from flask import Flask, request, abort, send_from_directory
from flask_cors import CORS, cross_origin
from error import InputError, AccessError

import auth
import channel
import channels
import message
import user
import other
import data
import traceback
import standup

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(app=APP)

APP.config['CORS_HEADERS'] = 'Content-Type'
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#@cross_origin(origin="*")
def handle_request(func):
    def wrapper(*args, **kwargs):
        try:
            return json.dumps(func(*args, **kwargs))
        except KeyError:
            # 400
            with open('log.txt', 'a') as f:
                f.write(traceback.format_exc())
            abort(400)
        except AccessError as response:
            # 401 or 403
            if str(response) == '400 Bad Request: Invalid Token':
                abort(401)
            else:
                abort(403)
        except InputError:
            # 401
            with open('log.txt', 'a') as f:
                f.write(traceback.format_exc())
            abort(401)
        except Exception:
            # 500
            with open('log.txt', 'a') as f:
                f.write(traceback.format_exc())
            abort(500)

    wrapper.__name__ = func.__name__
    return wrapper

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("/auth/login", methods=["POST"])
@handle_request
def svr_auth_login():
    req = request.get_json()
    email = req['email']
    pwd = req['password']
    return auth.auth_login(email, pwd)

@APP.route("/auth/register", methods=["POST"])
@handle_request
def svr_auth_register():
    req = request.get_json()
    email = req['email']
    pwd = req['password']
    fname = req['name_first']
    lname = req['name_last']
    return auth.auth_register(email, pwd, fname, lname)

@APP.route("/auth/logout", methods=["POST"])
@handle_request
def svr_auth_logout():
    req = request.get_json()
    token = req['token']
    return auth.auth_logout(token)

@APP.route("/auth/passwordreset/request", methods=["POST"])
@handle_request
def svr_auth_pwd_request():
    req = request.get_json()
    email = req['email']
    return auth.auth_passwordreset_request(email)

@APP.route("/auth/passwordreset/reset", methods=["POST"])
@handle_request
def svr_auth_pwd_reset():
    req = request.get_json()
    code = req['reset_code']
    new_password = req['new_password']
    return auth.auth_passwordreset_reset(code, new_password)

@APP.route("/channel/invite", methods=["POST"])
@handle_request
def svr_channel_invite():
    req = request.get_json()
    token = req['token']
    channel_id = int(req['channel_id'])
    user_id = int(req['u_id'])
    return channel.channel_invite(token, channel_id, user_id)

@APP.route("/channel/details", methods=["GET"])
@handle_request
def svr_channel_details():
    req = request.args
    token = req['token']
    channel_id = int(req['channel_id'])
    url = request.base_url.replace("/channel/details", "/static/profile_images/")
    result = channel.channel_details(token, channel_id)
    for i in range(len(result['all_members'])):
        if result['all_members'][i]['profile_img_url'] != "":
            result['all_members'][i]['profile_img_url'] = url + \
            result['all_members'][i]['profile_img_url']
    return result

@APP.route("/channel/messages", methods=["GET"])
@handle_request
def svr_channel_messages():
    req = request.args
    token = req['token']
    channel_id = int(req['channel_id'])
    start = int(req['start'])
    return channel.channel_messages(token, channel_id, start)

@APP.route("/channel/leave", methods=["POST"])
@handle_request
def svr_channel_leave():
    req = request.get_json()
    token = req['token']
    channel_id = int(req['channel_id'])
    return channel.channel_leave(token, channel_id)

@APP.route("/channel/join", methods=["POST"])
@handle_request
def svr_channel_join():
    req = request.get_json()
    token = req['token']
    channel_id = int(req['channel_id'])
    return channel.channel_join(token, channel_id)

@APP.route("/channel/addowner", methods=["POST"])
@handle_request
def svr_channel_addowner():
    req = request.get_json()
    token = req['token']
    channel_id = int(req['channel_id'])
    user_id = int(req['u_id'])
    return channel.channel_addowner(token, channel_id, user_id)

@APP.route("/channel/kickmember", methods=["POST"])
@handle_request
def svr_channel_kickmember():
    req = request.get_json()
    token = req['token']
    channel_id = int(req['channel_id'])
    user_id = int(req['u_id'])
    return channel.channel_kickmember(token, channel_id, user_id)

@APP.route("/channel/setnsfw", methods=["POST"])
@handle_request
def svr_channel_setnsfw():
    req = request.get_json()
    token = req['token']
    channel_id = int(req['channel_id'])
    nsfw = bool(req['is_nsfw'])
    return channel.channel_kickmember(token, channel_id, nsfw)


@APP.route("/channel/removeowner", methods=["POST"])
@handle_request
def svr_channel_removeowner():
    req = request.get_json()
    token = req['token']
    channel_id = int(req['channel_id'])
    user_id = int(req['u_id'])
    return channel.channel_removeowner(token, channel_id, user_id)


@APP.route("/channels/list", methods=["GET"])
@handle_request
def svr_channels_list():
    req = request.args
    token = req['token']
    return channels.channels_list(token)

@APP.route("/channels/listall", methods=["GET"])
@handle_request
def svr_channels_listall():
    req = request.args
    token = req['token']
    return channels.channels_listall(token)

@APP.route("/channels/create", methods=["POST"])
@handle_request
def svr_channels_create():
    req = request.get_json()
    token = req['token']
    name = req['name']
    is_public = req['is_public']
    return channels.channels_create(token, name, is_public)

@APP.route("/message/send", methods=["POST"])
@handle_request
def svr_message_send():
    req = request.get_json()
    token = req['token']
    channel_id = int(req['channel_id'])
    msg = req['message']
    return message.message_send(token, channel_id, msg)

@APP.route("/message/remove", methods=["DELETE"])
@handle_request
def svr_message_remove():
    req = request.get_json()
    token = req['token']
    message_id = int(req['message_id'])
    return message.message_remove(token, message_id)

@APP.route("/message/edit", methods=["PUT"])
@handle_request
def svr_message_edit():
    req = request.get_json()
    token = req['token']
    message_id = int(req['message_id'])
    msg = req['message']
    return message.message_edit(token, message_id, msg)

@APP.route("/message/sendlater", methods=["POST"])
@handle_request
def svr_message_sendlater():
    req = request.get_json()
    token = req['token']
    channel_id = int(req['channel_id'])
    msg = req['message']
    time_sent = int(req['time_sent'])
    return message.message_sendlater(token, channel_id, msg, time_sent)

@APP.route("/message/react", methods=["POST"])
@handle_request
def svr_message_react():
    req = request.get_json()
    token = req['token']
    message_id = int(req['message_id'])
    react_id = req['react_id']
    return message.message_react(token, message_id, react_id)

@APP.route("/message/unreact", methods=["POST"])
@handle_request
def svr_message_unreact():
    req = request.get_json()
    token = req['token']
    message_id = int(req['message_id'])
    react_id = req['react_id']
    return message.message_unreact(token, message_id, react_id)

@APP.route("/message/pin", methods=["POST"])
@handle_request
def svr_message_pin():
    req = request.get_json()
    token = req['token']
    message_id = int(req['message_id'])
    return message.message_pin(token, message_id)

@APP.route("/message/unpin", methods=["POST"])
@handle_request
def svr_message_unpin():
    req = request.get_json()
    token = req['token']
    message_id = int(req['message_id'])
    return message.message_unpin(token, message_id)

@APP.route("/user/profile", methods=["GET"])
@handle_request
def svr_user_profile():
    req = request.args
    token = req['token']
    u_id = int(req['u_id'])
    url = request.base_url.replace("/user/profile", "/static/profile_images/")
    result = user.user_profile(token, u_id)
    if result['user']['profile_img_url'] != "":
        result['user']['profile_img_url'] = url + \
        result['user']['profile_img_url']
    return result

@APP.route("/user/profile/setname", methods=["PUT"])
@handle_request
def svr_user_profile_setname():
    req = request.get_json()
    token = req['token']
    fname = req['name_first']
    lname = req['name_last']
    return user.user_profile_setname(token, fname, lname)

@APP.route("/user/profile/setemail", methods=["PUT"])
@handle_request
def svr_user_profile_setemail():
    req = request.get_json()
    token = req['token']
    email = req['email']
    return user.user_profile_setemail(token, email)

@APP.route("/user/profile/sethandle", methods=["PUT"])
@handle_request
def svr_user_profile_sethandle():
    req = request.get_json()
    token = req['token']
    handle = req['handle_str']
    return user.user_profile_sethandle(token, handle)

@APP.route("/user/profile/uploadphoto", methods=["POST"])
@handle_request
def svr_user_profile_uploadphoto():
    req = request.get_json()
    token = req['token']
    url = str(req['img_url'])
    x_start = int(req.get('x_start')) if req.get('x_start') else None
    y_start = int(req.get('y_start')) if req.get('y_start') else None
    x_end = int(req.get('x_end')) if req.get('x_end') else None
    y_end = int(req.get('y_end')) if req.get('y_end') else None
    return user.user_profile_uploadphoto(token, url, x_start, y_start, x_end, y_end)

@APP.route("/users/all", methods=["GET"])
@handle_request
def svr_users_all():
    req = request.args
    token = req['token']
    url = request.base_url.replace("/users/all", "/static/profile_images/")
    result = other.users_all(token)
    for i in range(len(result)):
        if result['users'][i]['profile_img_url'] != "":
            result['users'][i]['profile_img_url'] = url + \
            result['users'][i]['profile_img_url']
    return result

@APP.route("/admin/userpermission/change", methods=["POST"])
@handle_request
def svr_admin_userpermission_change():
    req = request.get_json()
    token = req['token']
    try:
        u_id = int(req['u_id'])
        p_id = int(req['permission_id'])
    except ValueError:
        raise InputError("Invalid parameters")
    return other.admin_userpermission_change(token, u_id, p_id)

@APP.route("/search", methods=["GET"])
@handle_request
def svr_search():
    req = request.args
    token = req['token']
    query = req['query_str']
    return other.search(token, query)

@APP.route("/clear", methods=["DELETE"])
@handle_request
def svr_clear():
    return other.clear()

@APP.route("/standup/start", methods=["POST"])
@handle_request
def svr_standup_start():
    req = request.get_json()
    token = req['token']
    channel_id = int(req['channel_id'])
    length = int(req['length'])
    return standup.standup_start(token, channel_id, length)

@APP.route("/standup/active", methods=["GET"])
@handle_request
def svr_standup_active():
    req = request.args
    token = req['token']
    channel_id = int(req['channel_id'])

    return standup.standup_active(token, channel_id)


@APP.route("/standup/send", methods=["POST"])
@handle_request
def svr_standup_send():
    req = request.get_json()
    token = req['token']
    channel_id = int(req['channel_id'])
    message = req['message']
    return standup.standup_send(token, channel_id, message)

if __name__ == "__main__":
    port_num = os.getenv('PORT')
    if port_num != None:
        print("port: ", port_num)
        APP.run(host='0.0.0.0', port=port_num) # Do not edit this port
    elif os.getenv('DEV'):
        APP.run(port=8080)
    else:
        APP.run(port=0) # Debugger
