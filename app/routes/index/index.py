from app import app
from app.routes.helper import validate_auth_token
from flask import render_template

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