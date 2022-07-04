from app import app, db
from app.models import User
from flask import abort, jsonify, make_response, request

import json

# Register function
# Adds new user if the user is not registered to database
@app.route('/register', methods=['POST'])
def register():
    # Get Request Data
    postRequest = json.loads(request.data)
    
    # Form validation
    if 'username' not in postRequest or 'email' not in postRequest or 'password' not in postRequest:
        abort(make_response(jsonify(message="Form is not complete"), 400))
    username = postRequest['username']
    email = postRequest['email']
    password = postRequest['password']
    if User.query.filter_by(username = username).first() is not None:
        abort(make_response(jsonify(message="Username exists"), 400))
    if User.query.filter_by(email = email).first() is not None:
        abort(make_response(jsonify(message="Email exists"), 400))

    # Execute insert user
    user = User(username = username, email = email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # Return the user token
    token = user.generate_auth_token()
    return jsonify({
        'username': user.username,
        'token': token
    }), 200