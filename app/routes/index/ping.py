from app import app

# Ping function
@app.route('/ping')
def ping():
    return 'pong'
