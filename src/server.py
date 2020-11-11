import sys
import os
import json
from json import dumps
from flask import Flask, request, abort
from flask_cors import CORS
from error import InputError, AccessError

import auth
import channel
import channels
import message
import user
import other
import data
import traceback

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
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

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
def svr_auth_login():
    try:
        req = request.get_json()
        email = req['email']
        pwd = req['password']
        return json.dumps(auth.auth_login(email, pwd))
    except KeyError:
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except:
        # 500
        abort(500)

@APP.route("/auth/register", methods=["POST"])
def svr_auth_register():
    try:
        req = request.get_json()
        email = req['email']
        pwd = req['password']
        fname = req['name_first']
        lname = req['name_last']
        return json.dumps(auth.auth_register(email, pwd, fname, lname))
    except KeyError:
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except Exception:
        # 500
        abort(500)

@APP.route("/auth/logout", methods=["POST"])
def svr_auth_logout():
    try:
        req = request.get_json()
        token = req['token']
        return json.dumps(auth.auth_logout(token))
    except KeyError: 
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except:
        # 500
        abort(500)

@APP.route("/channel/invite", methods=["POST"])
def svr_channel_invite():
    try:
        req = request.get_json()
        token = req['token']
        channel_id = int(req['channel_id'])
        user_id = int(req['u_id'])
        return json.dumps(channel.channel_invite(token, channel_id, user_id))
    except KeyError: 
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except:
        # 500
        abort(500)

@APP.route("/channel/details", methods=["GET"])
def svr_channel_details():
    try:
        req = request.args
        token = req['token']
        channel_id = int(req['channel_id'])
        return json.dumps(channel.channel_details(token, channel_id))
    except KeyError as response: 
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except:
        # 500
        abort(500)

@APP.route("/channel/messages", methods=["GET"])
def svr_channel_messages():
    try:
        req = request.args
        token = req['token']
        channel_id = int(req['channel_id'])
        start = int(req['start'])
        return json.dumps(channel.channel_messages(token, channel_id, start))
    except KeyError: 
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except:
        # 500
        abort(500)

@APP.route("/channel/leave", methods=["POST"])
def svr_channel_leave():
    try:
        req = request.get_json()
        token = req['token']
        channel_id = int(req['channel_id'])
        return json.dumps(channel.channel_leave(token, channel_id))
    except KeyError:
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except:
        # 500
        abort(500)


@APP.route("/channel/join", methods=["POST"])
def svr_channel_join():
    try:
        req = request.get_json()
        token = req['token']
        channel_id = int(req['channel_id'])
        return json.dumps(channel.channel_join(token, channel_id))
    except KeyError: 
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except:
        # 500
        abort(500)


@APP.route("/channel/addowner", methods=["POST"])
def svr_channel_addowner():
    try:
        req = request.get_json()
        token = req['token']
        channel_id = int(req['channel_id'])
        user_id = int(req['u_id'])
        return json.dumps(channel.channel_addowner(token, channel_id, user_id))
    except KeyError: 
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except:
        # 500
        abort(500)



@APP.route("/channel/removeowner", methods=["POST"])
def svr_channel_removeowner():
    try:
        req = request.get_json()
        token = req['token']
        channel_id = int(req['channel_id'])
        user_id = int(req['u_id'])
        return json.dumps(channel.channel_removeowner(token, channel_id, user_id))
    except KeyError: 
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except:
        # 500
        abort(500)


@APP.route("/channels/list", methods=["GET"])
def svr_channels_list():
    try:
        req = request.args
        token = req['token']
        res = channels.channels_list(token)
        return json.dumps(res)
    except KeyError: 
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except:
        # 500
        abort(500)

@APP.route("/channels/listall", methods=["GET"])
def svr_channels_listall():
    try:
        req = request.args
        token = req['token']
        return json.dumps(channels.channels_listall(token))
    except KeyError:
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except:
        # 500
        abort(500)

@APP.route("/channels/create", methods=["POST"])
def svr_channels_create():
    try:
        req = request.get_json()
        token = req['token']
        name = req['name']
        is_public = req['is_public']
        return json.dumps(channels.channels_create(token, name, is_public))
    except KeyError:
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except:
        # 500
        abort(500)

@APP.route("/message/send", methods=["POST"])
def svr_message_send():
    try:
        req = request.get_json()
        token = req['token']
        channel_id = int(req['channel_id'])
        msg = req['message']
        return json.dumps(message.message_send(token, channel_id, msg))
    except KeyError:
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except Exception as e:
        # 500
        with open('log.txt', 'a') as f:
            f.write(str(e))
        abort(500)


@APP.route("/message/remove", methods=["DELETE"])
def svr_message_remove():
    try:
        req = request.get_json()
        token = req['token']
        message_id = int(req['message_id'])
        return json.dumps(message.message_remove(token, message_id))
    except KeyError:
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except:
        # 500
        abort(500)


@APP.route("/message/edit", methods=["PUT"])
def svr_message_edit():
    try:
        req = request.get_json()
        token = req['token']
        message_id = int(req['message_id'])
        msg = req['message']
        return json.dumps(message.message_edit(token, message_id, msg))
    except KeyError:
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except:
        # 500
        abort(500)


@APP.route("/user/profile", methods=["GET"])
def svr_user_profile():
    try:
        req = request.args
        token = req['token']
        u_id = int(req['u_id'])
        return json.dumps(user.user_profile(token, u_id))
    except KeyError:
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except:
        # 500
        abort(500)
    finally:
        print(data.data)

@APP.route("/user/profile/setname", methods=["PUT"])
def svr_user_profile_setname():
    try:
        req = request.get_json()
        token = req['token']
        fname = req['name_first']
        lname = req['name_last']
        return json.dumps(user.user_profile_setname(token, fname, lname))
    except KeyError:
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except:
        # 500
        abort(500)

@APP.route("/user/profile/setemail", methods=["PUT"])
def svr_user_profile_setemail():
    try:
        req = request.get_json()
        token = req['token']
        email = req['email']
        return json.dumps(user.user_profile_setemail(token, email))
    except KeyError:
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except:
        # 500
        abort(500)


@APP.route("/user/profile/sethandle", methods=["PUT"])
def svr_user_profile_sethandle():
    try:
        req = request.get_json()
        token = req['token']
        handle = req['handle_str']
        return json.dumps(user.user_profile_sethandle(token, handle))
    except KeyError:
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except:
        # 500
        abort(500)

@APP.route("/users/all", methods=["GET"])
def svr_users_all():
    try:
        req = request.args
        token = req['token']
        return json.dumps(other.users_all(token))
    except KeyError:
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except:
        # 500
        abort(500)


@APP.route("/admin/userpermission/change", methods=["POST"])
def svr_admin_userpermission_change():
    try:
        req = request.get_json()
        token = req['token']
        try:
            u_id = int(req['u_id'])
            p_id = int(req['permission_id'])
        except ValueError:
            raise InputError("Invalid parameters")
        return json.dumps(other.admin_userpermission_change(token, u_id, p_id))
    except KeyError:
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except Exception:
        # 500
        abort(500)


@APP.route("/search", methods=["GET"])
def svr_search():
    try:
        req = request.args
        token = req['token']
        query = req['query_str']
        return json.dumps(other.search(token, query))
    except KeyError:
        # 400
        abort(400)
    except InputError:
        # 401
        abort(401)
    except AccessError as response:
        # 401 or 403
        if str(response) == '400 Bad Request: Invalid Token':
            abort(401)
        else:
            abort(403)
    except:
        # 500
        abort(500)


@APP.route("/clear", methods=["DELETE"])
def svr_clear():
    try:
        return json.dumps(other.clear())
    except:
        # 500
        abort(500)

if __name__ == "__main__":
    port_num = int(os.getenv('PORT'))
    port_num = 0 if port_num == None else port_num
    APP.run(port=port_num) # Do not edit this port
    #APP.run(port=8080, debug=True) # Debugger
