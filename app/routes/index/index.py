from app import app
from app.routes.helper import validate_auth_token
from flask import abort, jsonify, make_response, render_template

# Index function
# Returns simple html (can be rendered in browser)
@app.route('/')
@app.route('/index')
@validate_auth_token
def index(user):
    # Unauthorized access
    if user is None:
        abort(make_response(jsonify(message="Unauthorized"), 401))
    
    # Return scripted page
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