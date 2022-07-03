from flask import Flask, jsonify, request
from mysql import connector as mariadb
import json

app = Flask(__name__)
mydb = mariadb.connect(host='localhost', user='root', database='db-sks-dosen')

@app.route('/ping')
def ping():
    return jsonify({"message": "pong"})

@app.route('/test')
def test_get_database():
    cur = mydb.cursor(buffered=True)
    cur.execute('SELECT * FROM `users` WHERE username = %s', ["root"])

    for (user_id, username, password) in cur:
        print("User ID", user_id)
        print("Username", username)
        print("Password", password)
    
    return 'Bruh'

@app.route('/')
def index():
    return 'Dashboard'

@app.route('/login', methods=['POST'])
def login():
    # Get Request Dat
    postRequest = json.loads(request.data)
    username = postRequest['username']
    password = postRequest['password']

    # Cursor database
    cur = mydb.cursor(buffered=True)
    cur.execute('SELECT * FROM `users` WHERE username = %s', [username])

    # Invalid username check
    if cur.rowcount < 1:
        return "Failed to login"

    # Invalid password check
    user = cur.fetchone()
    if user[2] != password:
        return "Failed to Login"

    return 'Successful Login'

@app.route('/register', methods=['POST'])
def register():
    # Get Request Data
    postRequest = json.loads(request.data)
    username = postRequest['username']
    password = postRequest['password']

    # Execute insert user
    failed = False
    cur = mydb.cursor(buffered=True)

    try:
        cur.execute('INSERT INTO `users` (username, password) VALUES (%s, %s)', (username, password))
        mydb.commit()
    except mariadb.Error as error:
        print("Failed to register because of:", error)
        failed = True
        mydb.rollback()

    cur.close()

    if failed:
        return 'Failed Register'
    return 'Successful Register'