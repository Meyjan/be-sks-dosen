from app import app
from app.models import User
from app.routes.helper import convert_to_string
from flask import abort, jsonify, make_response, request

from app.routes.user.const import *
import json

# Constants

'''
Login function
Checks the user is logged in or not
Then if the username / password is correct, get the user token
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Get Request Data
    postRequest = json.loads(request.data)

    # Form validation
    if PARAM_USERNAME not in postRequest or PARAM_PASSWORD not in postRequest:
        abort(make_response(jsonify(message=ERR_FORM_IS_NOT_COMPLETE), 400))
    username, err = convert_to_string(postRequest[PARAM_USERNAME])
    if err is not None:
        abort(make_response(jsonify(message=ERR_FORM_INVALID_TYPE, developer_message=f'Invalid {PARAM_USERNAME} type'), 400))
    password, err = convert_to_string(postRequest[PARAM_PASSWORD])
    if err is not None:
        abort(make_response(jsonify(message=ERR_FORM_INVALID_TYPE, developer_message=f'Invalid {PARAM_PASSWORD} type'), 400))
    username = str(username)
    password = str(password)
    
    # Check if user and password is in database
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(make_response(jsonify(message=ERR_INVALID_USERNAME_PASSWORD), 200))
    if not user.check_password(password):
        abort(make_response(jsonify(message=ERR_INVALID_USERNAME_PASSWORD), 200))

    # Return the user token
    token = user.generate_auth_token()
    return jsonify({
        PARAM_USERNAME: user.username,
        PARAM_EMAIL: user.email,
        PARAM_TOKEN: token
    }), 200