from app import app, db
from app.models import User
from app.routes.helper import convert_to_string, validate_auth_token
from flask import abort, jsonify, make_response, request

import json

from app.routes.user.const import *

'''
Insert user function
Adds new user if the user is not registered to database
Like register but allows to check for the role
'''
@app.route('/user/insert', methods=['POST'])
@validate_auth_token
def insert_user(requester: User):
    # Making sure the user is admin
    if requester.roles != ROLE_ADMIN:
        abort(make_response(jsonify(message=ERR_ADMIN_REQUIRED), 401))

    # Get Request Data
    postRequest = json.loads(request.data)
    
    # Form validation
    if PARAM_USERNAME not in postRequest or PARAM_EMAIL not in postRequest or PARAM_PASSWORD not in postRequest or PARAM_ROLES not in postRequest:
        abort(make_response(jsonify(message=ERR_FORM_IS_NOT_COMPLETE), 400))
    username, err = convert_to_string(postRequest[PARAM_USERNAME])
    if err is not None:
        abort(make_response(jsonify(message=ERR_FORM_INVALID_TYPE, developer_message=f'Invalid {PARAM_USERNAME} type'), 400))
    email, err = convert_to_string(postRequest[PARAM_EMAIL])
    if err is not None:
        abort(make_response(jsonify(message=ERR_FORM_INVALID_TYPE, developer_message=f'Invalid {PARAM_EMAIL} type'), 400))
    password, err = convert_to_string(postRequest[PARAM_PASSWORD])
    if err is not None:
        abort(make_response(jsonify(message=ERR_FORM_INVALID_TYPE, developer_message=f'Invalid {PARAM_PASSWORD} type'), 400))
    roles, err = convert_to_string(postRequest[PARAM_ROLES])
    if err is not None:
        abort(make_response(jsonify(message=ERR_FORM_INVALID_TYPE, developer_message=f'Invalid {PARAM_ROLES} type'), 400))

    username = str(username)
    email = str(email)
    password = str(password)
    roles = str(roles)
    if roles not in [ROLE_ADMIN, ROLE_EDIT, ROLE_VIEW]:
        abort(make_response(jsonify(message=ERR_FORM_INVALID_TYPE, developer_message=f'Invalid {PARAM_ROLES} type'), 400))

    # Making sure the username and email doesn't exist in database
    if User.query.filter_by(username = username).first() is not None:
        abort(make_response(jsonify(message=ERR_USERNAME_EXISTS), 400))
    if User.query.filter_by(email = email).first() is not None:
        abort(make_response(jsonify(message=ERR_EMAIL_EXISTS), 400))

    # Execute insert user
    user = User(username = username, email = email, roles = roles)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # Return the user token
    token = user.generate_auth_token()
    return jsonify({
        PARAM_USERNAME: user.username,
        PARAM_TOKEN: token,
        PARAM_ROLES: roles
    }), 200