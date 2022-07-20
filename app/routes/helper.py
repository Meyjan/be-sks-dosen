from app import app
from app.models import User
from flask import jsonify, make_response, request
from functools import wraps

from app.routes.const import *

import jwt

# Verifying method (makes it static)
# Returns the user id about information
def validate_auth_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        # Validate if token exists in header
        if HEADER_ACCESS_TOKEN in request.headers:
            token = request.headers[HEADER_ACCESS_TOKEN]
        if not token:
            return make_response(jsonify(message=ERR_NO_TOKEN), 401)
        
        # Validate if the token is valid
        try:
            data = jwt.decode(token, app.config[KEY_SECRET], algorithms=[ALGO_ENCRYPT])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return make_response(jsonify(message=ERR_INVALID_TOKEN), 401)

        return f(current_user, *args, **kwargs)

    return decorator

# Verifying method (makes it static)
# Returns the user about information and makes sure the user have edit access
def validate_auth_token_edit_access(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        # Validate if token exists in header
        if HEADER_ACCESS_TOKEN in request.headers:
            token = request.headers[HEADER_ACCESS_TOKEN]
        if not token:
            return make_response(jsonify(message=ERR_NO_TOKEN), 401)
        
        # Validate if the token is valid
        try:
            data = jwt.decode(token, app.config[KEY_SECRET], algorithms=[ALGO_ENCRYPT])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return make_response(jsonify(message=ERR_INVALID_TOKEN), 401)
        
        if current_user.roles not in [ROLE_ADMIN, ROLE_EDIT]:
            return make_response(jsonify(message=ERR_NO_EDIT_ACCESS), 401)

        return f(current_user, *args, **kwargs)

    return decorator

# Verifying method (makes it static)
# Returns the user about information and makes sure the user have admin access
def validate_auth_token_admin_access(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        # Validate if token exists in header
        if HEADER_ACCESS_TOKEN in request.headers:
            token = request.headers[HEADER_ACCESS_TOKEN]
        if not token:
            return make_response(jsonify(message=ERR_NO_TOKEN), 401)
        
        # Validate if the token is valid
        try:
            data = jwt.decode(token, app.config[KEY_SECRET], algorithms=[ALGO_ENCRYPT])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return make_response(jsonify(message=ERR_INVALID_TOKEN), 401)
        
        if current_user.roles != ROLE_ADMIN:
            return make_response(jsonify(message=ERR_NO_ADMIN_ACCESS), 401)

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