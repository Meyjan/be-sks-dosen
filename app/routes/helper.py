from logging import error
from msilib.schema import Error
from app import app
from app.models import User
from flask import jsonify, make_response, request
from functools import wraps

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

# Verifying type string
# Returns true if the type is string, if not return error
def convert_to_string(x) -> tuple[str, Exception]:
    try:
        x_str = str(x)
        return x_str, None
    except ValueError:
        return "", ValueError