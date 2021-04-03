from flask import Flask, request
from app import app
import sqlite3,sys
from werkzeug.exceptions import HTTPException
import hashlib
import jwt
app = Flask(app)

con = sqlite3.connect('../database/hackiethon.db')
cur = con.cursor()
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
    query = '''BEGIN TRANSACTION;
                INSERT INTO user (token, username, password, email, name_first, name_last, level, xp) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', 0, 0);
               COMMIT;
            '''.format(token, data['username'], hashed_password, data['email'], data['name_first'], data['name_last'])
    cur.execute(query)
    return {'token': token}

@app.route('/task/create', methods=['POST'])
def task_create():
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
    query = '''BEGIN TRANSACTION;
                INSERT INTO task (task_id, title, description, xp, is_custom) VALUES ({}, '{}', '{}', {}, {});
               COMMIT;
            '''.format(task_id, data['title'], data['description'], task_xp, True)
    cur.execute(query)
    # # Insert task into user task list
    # query = '''BEGIN TRANSACTION;
    #             INSERT INTO active_task (token, task_id) VALUES ({}, {});
    #            COMMIT;
    #         '''.format(task_id, data['token'], data['task_id'])
    # cur.execute(query)
    return {'task_id': task_id}

@app.route('/task/edit', methods=['PUT'])
def task_edit():
    data = request.get_json()
    if data['title'] is None:
        raise InputError ("Please enter a title")
    query = '''BEGIN TRANSACTION;
                UPDATE task t
                SET  t.title = '{}',
                        t.description = '{}'
                WHERE t.task_id = {};
                COMMIT;'''.format(data['title'], data['description'], data['task_id'])
    cur.execute(query)
    return {}

@app.route('/task/remove', methods=['DELETE'])
def task_remove():
    data = request.get_json()
    if data['task_id'] is None:
        raise NotFound ("Task not found")
    query = '''BEGIN TRANSACTION;
                DELETE FROM active_task t
                WHERE t.task_id = {} and t.token = '{}';
                COMMIT;'''.format(data['task_id'], data['token'])
    cur.execute(query)
    query = '''BEGIN TRANSACTION;
                DELETE FROM task t
                WHERE t.task_id = {};
                COMMIT;'''.format(data['task_id'])
    cur.execute(query)
    return {}

# @app.route('/task/finish', methods=['PUT'])
# def task_finish():
#     xp_threshold = 50
#     new_level = 0
#     new_xp = 0
#     data = request.get_json()
#     if data['token'] is None:
#         raise AccessError ("Invalid Token")
#     if data['task_id'] is None:
#         raise NotFound ("Task not found")
#     query = '''select u.token from user.u where u.token = '{}';'''.format(data['token'])
#     cur.execute(query)
#     x = cur.fetchone()
#     if x is None:
#         raise AccessError ("Invalid Token")
#     query = '''BEGIN TRANSACTION;
#                 UPDATE active_task t
#                 SET  is_completed = True
#                 WHERE t.token = '{}';
#                 COMMIT;'''.format(data['token'])
#     cur.execute(query)
#     cur.execute('''select t.task_xp from task t where t.task_id = {};'''.format(data['task_id']))
#     task_xp = cur.fetchone
#     query = '''select u.level, u.xp from user u where u.token = '{}';'''.format(data['token'])
#     x = cur.fetchone()
#     level, xp = x
#     if xp + task_xp >= xp_threshold:
#         new_xp = (xp + task_xp) - xp_threshold
#         new_level = level + 1
#     else:
#         new_xp = xp + task_xp
#         new_level = level
#     query = ''' BEGIN TRANSACTION;
#                     UPDATE user u
#                         SET u.level = {},
#                             u.xp = {}
#                     WHERE u.token = '{}';
#                 COMMIT;'''.format(new_level, new_xp, data['token'])
#     cur.execute(query)

#     return {}

@app.route('/task/gettasks', methods=['GET'])
def task_finish():
    return {}

@app.route('/user/list', methods=['GET'])
def task_finish():
    return {}

@app.route('/user/details', methods=['GET'])
def task_finish():
    return {}

if __name__ == '__main__':
    app.run(debug=True, port=5500)