from flask import Flask, request
import sqlite3,sys
from werkzeug.exceptions import HTTPException
import hashlib
import jwt
app = Flask(__name__)

con = sqlite3.connect('../database/hackiethon.db')
cur = con.cursor()
class ConflictError(HTTPException):
    code = 409
    message = 'No message specified'

class AccessError(HTTPException):
    code = 403
    message = 'No message specified'

class InputError(HTTPException):
    code = 400
    message = 'No message specified'

def hasher(string):
    return hashlib.sha256(string.encode()).hexdigest()

# Generates a token for a registered user
def generate_token(username):
    '''
    Generates a JSON Web Token (JWT) encoded token for a given username
    Input: username (str)
    Output: JWT-encoded token (str)
    '''
    private_key = 'HamsterHealthIsTheBestWebsite'
    return jwt.encode({'username': username}, private_key, algorithm='HS256').decode('utf-8')

@app.route('/auth/login', methods=['POST'])
def auth_login():
    data = request.get_json()
    if data['username'] is None or data['password'] is None:
        raise InputError ('Please enter your username and password')
    query = ''''select u.token, u.password from user u where u.username = '{}'; '''.format(data['username'])
    cur.execute(query)
    x = cur.fetchone()
    if x is None:
        raise AccessError ('Invalid username')
    token,password = x
    hashed_password = hasher(data['username'])
    if hashed_password != password:
        raise AccessError ('Incorrect password')
    return {'token': token}

@app.route('/auth/register', methods=['POST'])
def auth_register():
    data = request.get_json()
    if data['username'] is None or data['password'] is None or data['name'] is None or data['email'] is None:
        raise InputError ('Please fill in all details')

    # Checks if username is unique
    query = ''''select u.username from user u where u.username = '{}'; '''.format(data['username'])
    cur.execute(query)
    x = cur.fetchone()
    if x is not None:
        raise ConflictError ('Username already taken')

    # Checks if email is unique
    query = ''''select u.email from user u where u.email = '{}'; '''.format(data['email'])
    cur.execute(query)
    x = cur.fetchone()
    if x is not None:
        raise ConflictError ('Email already in use')

    hashed_password = hasher(data['password'])
    token = generate_token(data['username'])
    query = '''INSERT INTO user (token, username, password, email, name_first, name_last) values ({}, {}, {}, {}, {}, {});
            '''.format(token, data['username'], hashed_password, data['email'], data['name_first'], data['name_last'])
    cur.execute(query)
    return {'token': token}

@app.route('/task/create', methods=['POST'])
def task_create():
    return {}

@app.route('/task/edit', methods=['PUT'])
def task_edit():
    return {}

@app.route('/task/remove', methods=['DELETE'])
def task_remove():
    return {}

@app.route('/task/finish', methods=['PUT'])
def task_finish():
    return {}

@app.route('/task/gettasks', methods=['GET'])
def task_finish():
    return {}

@app.route('/user/list', methods=['GET'])
def task_finish():
    return {}

@app.route('/user/details', methods=['GET'])
def task_finish():
    return {}