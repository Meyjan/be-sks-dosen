from wsgiref import validate
from app import app, db
from app.models import User
from flask import abort, jsonify, make_response, render_template, request
from functools import wraps

import json
import jwt

# Verifying method (makes it static)
# Returns the user id about information
def validate_auth_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        # Validate if token exists in header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify(message="A valid token is missing!"), 401)
        
        # Validate if the token is valid
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return make_response(jsonify(message="Invalid token!"), 401)

        return f(current_user, *args, **kwargs)

    return decorator

# Index function
# Returns simple html (can be rendered in browser)
@app.route('/')
@app.route('/index')
@validate_auth_token
def index(user):
    user = {'username': user.username}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

# Ping function
@app.route('/ping')
def ping():
    return 'pong'

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