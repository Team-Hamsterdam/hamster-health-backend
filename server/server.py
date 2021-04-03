from flask import Flask, request, make_response
from flask_cors import CORS
import sqlite3,sys
from werkzeug.exceptions import HTTPException
import hashlib
import jwt
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)


class ConflictError(HTTPException):
    code = 409
    message = 'No message specified'

class NotFound(HTTPException):
    code = 404
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
    return jwt.encode({'username': username}, private_key, algorithm='HS256')

# @app.after_request
# def after_request_func(response):
#     response = make_response()
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     response.headers.add("Access-Control-Allow-Headers", "*")
#     response.headers.add("Access-Control-Allow-Methods", "*")
#     return response


@app.route('/auth/login', methods=['POST'])
@cross_origin()
def auth_login():
    con = sqlite3.connect('../database/hackiethon.db')
    cur = con.cursor()
    data = request.get_json()
    if data['username'] is None or data['password'] is None:
        raise InputError ('Please enter your username and password')
    query = '''select u.token, u.password from user u where u.username = "{}"; '''.format(data['username'])
    cur.execute(query)
    x = cur.fetchone()
    if x is None:
        raise AccessError ('Invalid username')
    token,password = x
    hashed_password = hasher(data['username'])
    if hashed_password != password:
        raise AccessError ('Incorrect password')

    cur.execute('BEGIN TRANSACTION;')
    cur.execute('''UPDATE user set logged_in = 1 where user.token = "{}";'''.format(token))
    cur.execute('COMMIT;')

    return {'token': token}

@app.route('/auth/register', methods=['POST'])
@cross_origin()
def auth_register():
    con = sqlite3.connect('../database/hackiethon.db')
    cur = con.cursor()
    data = request.get_json()
    if data['username'] is None or data['password'] is None or data['name'] is None or data['email'] is None:
        raise InputError ('Please fill in all details')
    print(data)
    # Checks if username is unique
    query = '''select u.username from user u where u.username = "{}"; '''.format(data['username'])
    cur.execute(query)
    x = cur.fetchone()
    if x is not None:
        raise ConflictError ('Username already taken')

    # Checks if email is unique
    query = '''select u.email from user u where u.email = "{}"; '''.format(data['email'])
    cur.execute(query)
    x = cur.fetchone()
    if x is not None:
        raise ConflictError ('Email already in use')

    hashed_password = hasher(data['password'])
    token = generate_token(data['username'])
    cur.execute('BEGIN TRANSACTION;')
    query = '''
                INSERT INTO user (token, username, password, email, name, level, xp) VALUES ("{}", "{}", "{}", "{}", "{}", 0, 0);

            '''.format(token, data['username'], hashed_password, data['email'], data['name'])
    cur.execute(query)
    cur.execute('COMMIT;')
    return {'token': token}

@app.route('/auth/check', methods=['GET'])
@cross_origin()
def auth_check():
    con = sqlite3.connect('../database/hackiethon.db')
    cur = con.cursor()
    data = request.get_json()
    if data['token'] is None:
        raise AccessError ("Invalid Token")
    query = '''select u.logged_in from user.u where u.token = "{}";'''.format(data['token'])
    cur.execute(query)
    x = cur.fetchone()
    if x is None:
        raise AccessError ("Invalid Token")
    if x is False:
        raise AccessError ("User not logged in")
    return {'token': data['token']}

@app.route('/task/create', methods=['POST'])
@cross_origin()
def task_create():
    con = sqlite3.connect('../database/hackiethon.db')
    cur = con.cursor()
    data = request.get_json()
    if data['title'] is None:
        raise InputError ("Please enter a title")
    # Generate task_id
    task_id = 0
    query = '''select count(t.task_id) from task t;'''
    cur.execute(query)
    task_id = cur.fetchone()
    task_xp = 5
    # Insert task into database
    cur.execute('BEGIN TRANSACTION;')
    query = '''INSERT INTO task (task_id, title, description, xp, is_custom) VALUES ({}, "{}", "{}", {}, {});'''.format(task_id, data['title'], data['description'], task_xp, True)
    cur.execute(query)
    cur.execute('COMMIT;')
    # # Insert task into user task list
    # query = '''BEGIN TRANSACTION;
    #             INSERT INTO active_task (token, task_id) VALUES ({}, {});
    #            COMMIT;
    #         '''.format(task_id, data['token'], data['task_id'])
    # cur.execute(query)
    return {'task_id': task_id}

@app.route('/task/edit', methods=['PUT'])
@cross_origin()
def task_edit():
    con = sqlite3.connect('../database/hackiethon.db')
    cur = con.cursor()
    data = request.get_json()
    if data['title'] is None:
        raise InputError ("Please enter a title")
    cur.execute('BEGIN TRANSACTION;')
    query = '''UPDATE task t
                SET  t.title = "{}",
                        t.description = "{}"
                WHERE t.task_id = {};'''.format(data['title'], data['description'], data['task_id'])
    cur.execute(query)
    cur.execute('COMMIT;')
    return {}

@app.route('/task/remove', methods=['DELETE'])
@cross_origin()
def task_remove():
    con = sqlite3.connect('../database/hackiethon.db')
    cur = con.cursor()
    data = request.get_json()
    if data['task_id'] is None:
        raise NotFound ("Task not found")
    cur.execute('BEGIN TRANSACTION;')
    query = '''DELETE FROM active_task t
                WHERE t.task_id = {} and t.token = "{}";'''.format(data['task_id'], data['token'])
    cur.execute(query)
    cur.execute('COMMIT;')
    cur.execute('BEGIN TRANSACTION;')
    query = '''DELETE FROM task t
                WHERE t.task_id = {};'''.format(data['task_id'])
    cur.execute(query)
    cur.execute('COMMIT;')
    return {}

@app.route('/task/finish', methods=['PUT'])
@cross_origin()
def task_finish():
    con = sqlite3.connect('../database/hackiethon.db')
    cur = con.cursor()
    xp_threshold = 50
    new_level = 0
    new_xp = 0
    data = request.get_json()
    if data['token'] is None:
        raise AccessError ("Invalid Token")
    if data['task_id'] is None:
        raise NotFound ("Task not found")
    query = '''select u.token from user.u where u.token = "{}";'''.format(data['token'])
    cur.execute(query)
    x = cur.fetchone()
    if x is None:
        raise AccessError ("Invalid Token")
    cur.execute('BEGIN TRANSACTION;')
    query = '''UPDATE active_task t
                SET  is_completed = True
                WHERE t.token = "{}";'''.format(data['token'])
    cur.execute(query)
    cur.execute('COMMIT;')
    cur.execute('''select t.task_xp from task t where t.task_id = {};'''.format(data['task_id']))
    task_xp = cur.fetchone
    query = '''select u.level, u.xp from user u where u.token = "{}";'''.format(data['token'])
    x = cur.fetchone()
    level, xp = x
    if xp + task_xp >= xp_threshold:
        new_xp = (xp + task_xp) - xp_threshold
        new_level = level + 1
    else:
        new_xp = xp + task_xp
        new_level = level
    cur.execute('BEGIN TRANSACTION;')
    query = ''' UPDATE user u
                    SET u.level = {},
                        u.xp = {}
                WHERE u.token = "{}";'''.format(new_level, new_xp, data['token'])
    cur.execute(query)
    cur.execute('COMMIT;')

    return {}

@app.route('/task/gettasks', methods=['GET'])
@cross_origin()
def task_gettasks():
    tasks_list = []
    con = sqlite3.connect('../database/hackiethon.db')
    cur = con.cursor()
    data = request.get_json()
    if data['token'] is None:
        raise AccessError ("Invalid Token")
    query = '''select u.token from user.u where u.token = "{}";'''.format(data['token'])
    cur.execute(query)
    x = cur.fetchone()
    if x is None:
        raise AccessError ("Invalid Token")
    query = '''select t.task_id, t.title, t.description, t.task_xp t.is_custom from task
                join active_task active on active.task_id = t.task_id
                where active.token = {};'''.format(data['token'])
    while True:
        x = cur.fetchone()
        if x is None:
            break
        task_id, title, description, task_xp, is_custom = x
        task = {
            'task_id': task_id,
            'title': title,
            'description': description,
            'task_xp': task_xp,
            'is_custom': is_custom
        }
        tasks_list.append(task)


    return {"tasks": tasks_list}

@app.route('/user/list', methods=['GET'])
@cross_origin()
def user_list():
    con = sqlite3.connect('../database/hackiethon.db')
    cur = con.cursor()
    users_list = []
    data = request.get_json()
    if data['token'] is None:
        raise AccessError ("Invalid Token")
    query = '''select u.token from user.u where u.token = "{}";'''.format(data['token'])
    cur.execute(query)
    x = cur.fetchone()
    if x is None:
        raise AccessError ("Invalid Token")
    cur.execute('select u.username, u.level, u.xp from user u;')
    while True:
        x = cur.fetchone()
        if x is None:
            break
        username, level, xp = x
        user = {
            'username': username,
            'level': level,
            'xp': xp,
        }
        user_list.append(user)
    return {'users': users_list}

@app.route('/user/details', methods=['GET'])
@cross_origin()
def user_details():
    con = sqlite3.connect('../database/hackiethon.db')
    cur = con.cursor()
    data = request.get_json()
    if data['token'] is None:
        raise AccessError ("Invalid Token")
    query = '''select u.token from user.u where u.token = "{}";'''.format(data['token'])
    cur.execute(query)
    x = cur.fetchone()
    if x is None:
        raise AccessError ("Invalid Token")
    cur.execute('select u.username, u.level, u.xp from user u where u.token = "{}";').format(data['token'])
    x = cur.fetchone()
    username, level, xp = x
    user = {
        'username': username,
        'level': level,
        'xp': xp,
    }
    return {'users': user}

if __name__ == '__main__':
    app.run(debug=True, port=4000)