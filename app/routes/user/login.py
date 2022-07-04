from app import app
from app.models import User
from flask import abort, jsonify, make_response, request

import json

# Login function
# Checks the user is logged in or not
# Then if the username / password is correct, get the user token
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Get Request Data
    postRequest = json.loads(request.data)

    # Form validation
    if 'username' not in postRequest or 'password' not in postRequest:
        abort(make_response(jsonify(message="Form is not complete"), 400))
    username = postRequest['username']
    password = postRequest['password']
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(make_response(jsonify(message="Invalid username / password"), 400))
    if not user.check_password(password):
        abort(make_response(jsonify(message="Invalid username / password"), 400))

    # Return the user token
    token = user.generate_auth_token()
    return jsonify({
        'username': user.username,
        'token': token
    }), 200