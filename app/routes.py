from flask import render_template
from app import app

# Index function
# Returns simple html (can be rendered in browser)
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Meyjan'}
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