from app import app, db
from app.models import User
from app.routes.helper import convert_to_string
from flask import abort, jsonify, make_response, request

import json

from app.routes.user.const import *

'''
Register function
Adds new user if the user is not registered to database
'''
@app.route('/register', methods=['POST'])
def register():
    # Get Request Data
    postRequest = json.loads(request.data)
    
    # Form validation
    if PARAM_USERNAME not in postRequest or PARAM_EMAIL not in postRequest or PARAM_PASSWORD not in postRequest:
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
    username = str(username)
    email = str(email)
    password = str(password)

    # Making sure the username and email doesn't exist in database
    if User.query.filter_by(username = username).first() is not None:
        abort(make_response(jsonify(message=ERR_USERNAME_EXISTS), 400))
    if User.query.filter_by(email = email).first() is not None:
        abort(make_response(jsonify(message=ERR_EMAIL_EXISTS), 400))

    # Execute insert user
    user = User(username = username, email = email, roles = ROLE_VIEW)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # Return the user token
    token = user.generate_auth_token()
    return jsonify({
        PARAM_USERNAME: user.username,
        PARAM_TOKEN: token,
        PARAM_ROLES: ROLE_VIEW
    }), 200

'''
Register as admin function
Hidden function to register as an administrator
Used for testing only
Adds new user if the user is not registered to database
'''
@app.route('/register_admin', methods=['POST'])
def register_admin():
    # Get Request Data
    postRequest = json.loads(request.data)
    
    # Form validation
    if PARAM_USERNAME not in postRequest or PARAM_EMAIL not in postRequest or PARAM_PASSWORD not in postRequest:
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
    username = str(username)
    email = str(email)
    password = str(password)

    # Making sure the username and email doesn't exist in database
    if User.query.filter_by(username = username).first() is not None:
        abort(make_response(jsonify(message=ERR_USERNAME_EXISTS), 400))
    if User.query.filter_by(email = email).first() is not None:
        abort(make_response(jsonify(message=ERR_EMAIL_EXISTS), 400))

    # Execute insert user
    user = User(username = username, email = email, roles = ROLE_ADMIN)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # Return the user token
    token = user.generate_auth_token()
    return jsonify({
        PARAM_USERNAME: user.username,
        PARAM_TOKEN: token,
        PARAM_ROLES: ROLE_ADMIN
    }), 200