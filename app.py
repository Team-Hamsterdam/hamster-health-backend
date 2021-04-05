from flask import Flask, request, make_response, abort, jsonify
from flask_cors import CORS
import sys
import psycopg2
import urllib.parse as urlparse
from werkzeug.exceptions import HTTPException
import hashlib
import jwt
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# Uncomment and change if hosting locally
# os.environ['DATABASE_URL'] = "postgres://USERNAME:PASSWORD@localhost:5432/DBNAME"
url = urlparse.urlparse(os.environ['DATABASE_URL'])

dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

con = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
            )

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
    """
    Generates a JSON Web Token (JWT) encoded token for a given username
    Input: username (str)
    Output: JWT-encoded token (str)
    """
    private_key = "SecretKey"
    # private_key = os.environ['PRIVATE_KEY']
    token = jwt.encode({'username': username}, private_key, algorithm='HS256').decode("utf-8")
    return (token)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/auth/login', methods=['POST'])
@cross_origin()
def auth_login():
    cur = con.cursor()
    data = request.get_json()
    if data['username'] is None or data['password'] is None:
        # raise InputError ('Please enter your username and password')
        raise InvalidUsage('Please enter your username and password', status_code=400)
    query = """select u.token, u.password from user_table u where u.username = '{}'; """.format(data['username'])
    cur.execute(query)
    x = cur.fetchone()
    if x is None:
        # raise AccessError ('Invalid username')
        raise InvalidUsage('Invalid username', status_code=403)
    token,password = x
    hashed_password = hasher(data['password'])
    if hashed_password != password:
        # raise AccessError ('Incorrect password')
        raise InvalidUsage('Incorrect password', status_code=403)

    cur.execute('BEGIN TRANSACTION;')
    cur.execute("""UPDATE user_table set logged_in = 1 where user_table.token = '{}';""".format(token))
    cur.execute('COMMIT;')

    return {'token': token}

@app.route('/auth/register', methods=['POST'])
@cross_origin()
def auth_register():
    cur = con.cursor()
    data = request.get_json()
    if data['username'] is None or data['password'] is None or data['name'] is None or data['email'] is None:
        # raise InputError ('Please fill in all details')
        raise InvalidUsage('Please fill in all details', status_code=400)
    # Checks if username is unique
    query = """select u.username from user_table u where u.username = '{}'; """.format(data['username'])
    cur.execute(query)
    x = cur.fetchone()
    if x is not None:
        # abort (409, description='Username already taken')
        # return 'Username already taken', 409
        raise InvalidUsage('Username already taken', status_code=409)

    # Checks if email is unique
    query = """select u.email from user_table u where u.email = '{}'; """.format(data['email'])
    cur.execute(query)
    x = cur.fetchone()
    if x is not None:
        # abort (409, description='Email already in use')
        # return 'Email already in use', 409
        raise InvalidUsage('Email already taken', status_code=409)

    hashed_password = hasher(data['password'])
    token = generate_token(data['username'])
    cur.execute('BEGIN TRANSACTION;')
    query = """
                INSERT INTO user_table (token, username, password, email, name, level, xp) VALUES ('{}', '{}', '{}', '{}', '{}', 0, 0);
            """.format(token, data['username'], hashed_password, data['email'], data['name'])
    cur.execute(query)
    cur.execute('COMMIT;')
    return {'token': token}

@app.route('/auth/check', methods=['GET'])
@cross_origin()
def auth_check():
    cur = con.cursor()
    data = request.headers.get('Authorization')
    if data is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)
    query = """select u.logged_in from user_table u where u.token = '{}';""".format(data)
    cur.execute(query)
    x = cur.fetchone()
    if x is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)
    if x is False:
        # raise AccessError ("User not logged in")
        raise InvalidUsage('User not logged in', status_code=403)
    return {'token': data}

@app.route('/task/create', methods=['POST'])
@cross_origin()
def task_create():
    cur = con.cursor()
    parsed_token = request.headers.get('Authorization')
    data = request.get_json()
    if data['title'] is None:
        # raise InputError ("Please enter a title")
        raise InvalidUsage('Please enter a title', status_code=400)
    # Generate task_id
    task_id = 0
    query = """select max(t.task_id) from task t;"""
    cur.execute(query)
    x = cur.fetchone()
    task_id_tuple = x
    if x is None:
        task_id_tuple[0] = 1
    task_id = task_id_tuple[0]
    task_id += 1
    task_xp = 5
    # Insert task into database
    cur.execute('BEGIN TRANSACTION;')
    query = """INSERT INTO task (token, task_id, title, description, task_xp, is_custom)
                VALUES ('{}', {}, '{}', '{}', {}, {});""".format(parsed_token, task_id, data['title'], data['description'], task_xp, 1)
    cur.execute(query)
    cur.execute('COMMIT;')
    # Insert task into user task list
    # query = """BEGIN TRANSACTION;
    #             INSERT INTO active_task (token, task_id, title, description, is_completed) VALUES ('{}', {}, '{}', '{}', 0);
    #            COMMIT;
    #         """.format(data['token'], task_id, data['title'], data['description'])
    # cur.execute(query)
    return {'task_id': task_id}

@app.route('/task/edit', methods=['PUT'])
@cross_origin()
def task_edit():
    cur = con.cursor()
    data = request.get_json()
    if data['title'] is None:
        # raise InputError ("Please enter a title")
        raise InvalidUsage('Please enter a title', status_code=400)
    cur.execute('BEGIN TRANSACTION;')
    query = """UPDATE active_task t
                SET  t.title = '{}',
                     t.description = '{}'
                WHERE t.task_id = {};""".format(data['title'], data['description'], data['task_id'])
    cur.execute(query)
    cur.execute('COMMIT;')
    return {}

@app.route('/task/remove', methods=['DELETE'])
@cross_origin()
def task_remove():
    cur = con.cursor()
    parsed_token = request.headers.get('Authorization')
    data = request.get_json()
    if parsed_token is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)
    query = """select u.token from user_table u where u.token = '{}';""".format(parsed_token)
    cur.execute(query)
    x = cur.fetchone()
    if x is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)
    if data['task_id'] is None:
        # raise NotFound ("Task not found")
        raise InvalidUsage('Task not found', status_code=404)

    cur.execute('BEGIN TRANSACTION;')
    query = """DELETE FROM task
                WHERE task.task_id = {} and task.token = '{}';""".format(data['task_id'], parsed_token)
    cur.execute(query)
    cur.execute('COMMIT;')
    return {}

@app.route('/task/removeactivetask', methods=['DELETE'])
@cross_origin()
def task_removepersonal():
    cur = con.cursor()
    parsed_token = request.headers.get('Authorization')
    data = request.get_json()
    if parsed_token is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)
    query = """select u.token from user_table u where u.token = '{}';""".format(parsed_token)
    cur.execute(query)
    x = cur.fetchone()
    if x is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)
    if data['task_id'] is None:
        # raise NotFound ("Task not found")
        raise InvalidUsage('Task not found', status_code=404)
    cur.execute('BEGIN TRANSACTION;')
    query = """DELETE FROM active_task
                WHERE active_task.task_id = {} and active_task.token = '{}';""".format(data['task_id'], parsed_token)
    cur.execute(query)
    cur.execute('COMMIT;')
    return {}

@app.route('/task/addactivetask', methods=['POST'])
@cross_origin()
def task_add_active_task():
    cur = con.cursor()


    parsed_token = request.headers.get('Authorization')
    data = request.get_json()
    if parsed_token is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)
    query = """select u.token from user_table u where u.token = '{}';""".format(parsed_token)
    cur.execute(query)
    x = cur.fetchone()
    if x is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)

    # if data['task_id'] is None:
    #     raise NotFound ("Task not found")
    query = """select task.title, task.description from task
                where task.task_id = {};""".format(data['task_id'])
    cur.execute(query)
    x = cur.fetchone()
    if x is None:
        # raise NotFound ("Task not found")
        raise InvalidUsage('Task not found', status_code=404)
    title, description = x
    query = """select active_task.task_id from active_task
                where active_task.task_id = {} and active_task.token = '{}';""".format(data['task_id'], parsed_token)
    cur.execute(query)
    x = cur.fetchone()
    if x is not None:
        # raise ConflictError ("Task already chosen")
        raise InvalidUsage('Task already active', status_code=409)
    cur.execute('BEGIN TRANSACTION;')
    query = """INSERT INTO active_task (token, task_id, title, description, is_completed)
                VALUES ('{}', {}, '{}', '{}', 0);""".format(parsed_token, data['task_id'], title, description)
    cur.execute(query)
    cur.execute('COMMIT;')
    return {}

@app.route('/task/finish', methods=['PUT'])
@cross_origin()
def task_finish():
    cur = con.cursor()
    xp_threshold = 50
    new_level = 0
    new_xp = 0
    parsed_token = request.headers.get('Authorization')
    data = request.get_json()
    if parsed_token is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)
    if data['task_id'] is None:
        # raise NotFound ("Task not found")
        raise InvalidUsage('Task not found', status_code=404)
    query = """select u.token from user_table u where u.token = '{}';""".format(parsed_token)
    cur.execute(query)
    x = cur.fetchone()
    if x is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)
    cur.execute('BEGIN TRANSACTION;')
    query = """UPDATE active_task
                SET  is_completed = 1
                WHERE active_task.token = '{}';""".format(parsed_token)
    cur.execute(query)
    cur.execute('COMMIT;')
    cur.execute("""select task.task_xp from task where task.task_id = {};""".format(data['task_id']))
    x = cur.fetchone()
    task_xp = x
    query = """select u.level, u.xp from user_table u where u.token = '{}';""".format(parsed_token)
    cur.execute(query)
    x = cur.fetchone()
    level, user_xp = x
    if (user_xp + task_xp[0]) >= xp_threshold:
        new_xp = (user_xp + task_xp[0]) - xp_threshold
        new_level = level + 1
    else:
        new_xp = user_xp + task_xp[0]
        new_level = level
    cur.execute('BEGIN TRANSACTION;')
    query = """ UPDATE user_table
                    SET level = {},
                        xp = {}
                WHERE token = '{}';""".format(new_level, new_xp, parsed_token)
    cur.execute(query)
    cur.execute('COMMIT;')

    return {}

@app.route('/task/gettasks', methods=['GET'])
@cross_origin()
def task_gettasks():
    tasks_list = []
    cur = con.cursor()
    data = request.headers.get('Authorization')
    if data is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)
    query = """select u.token from user_table u where u.token = '{}';""".format(data)
    cur.execute(query)
    x = cur.fetchall()
    if x is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)
    query = """select task.task_id, task.title, task.description, task.task_xp, task.is_custom from task
                join active_task active on active.task_id = task.task_id
                where active.token = '{}';""".format(data)
    cur.execute(query)
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

@app.route('/task/getourtasks', methods=['GET'])
@cross_origin()
def task_get_our_tasks():
    tasks_list = []
    cur = con.cursor()
    data = request.headers.get('Authorization')
    if data is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)
    query = """select u.token from user_table u where u.token = '{}';""".format(data)
    cur.execute(query)
    x = cur.fetchall()
    if x is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)
    query = """select task.task_id, task.title, task.description, task.task_xp, task.is_custom from task
                where task.is_custom = 0;"""
    cur.execute(query)
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

@app.route('/task/getcustomtasks', methods=['GET'])
@cross_origin()
def task_get_custom_tasks():
    tasks_list = []
    cur = con.cursor()
    data = request.headers.get('Authorization')
    if data is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)
    query = """select u.token from user_table u where u.token = '{}';""".format(data)
    cur.execute(query)
    x = cur.fetchall()
    if x is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)
    query = """select task.task_id, task.title, task.description, task.task_xp, task.is_custom from task
                where task.is_custom = 1 and task.token = '{}';""".format(data)
    cur.execute(query)
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
    num_users = 50
    cur = con.cursor()
    users_list = []
    # data = request.get_json()
    parsed_token = request.headers.get('Authorization')
    if parsed_token is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)
    query = """select u.token from user_table u where u.token = '{}';""".format(parsed_token)
    cur.execute(query)
    x = cur.fetchone()
    if x is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)
    query = """SELECT user_table.username, user_table.level, user_table.xp
                FROM user_table
                ORDER BY user_table.level DESC, user_table.xp DESC
                LIMIT 50;"""
    cur.execute(query)
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
        users_list.append(user)
    return {'users': users_list}

@app.route('/user/details', methods=['GET'])
@cross_origin()
def user_details():
    cur = con.cursor()
    parsed_token = request.headers.get('Authorization')
    if parsed_token is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)
    query = """select u.token from user_table u where u.token = '{}';""".format(parsed_token)
    cur.execute(query)
    x = cur.fetchone()
    if x is None:
        # raise AccessError ("Invalid Token")
        raise InvalidUsage('Invalid Token', status_code=403)
    cur.execute("select u.username, u.level, u.xp from user_table u where u.token = '{}';".format(parsed_token))
    x = cur.fetchone()
    username, level, xp = x
    cur.execute('select count(*) from user_table where user_table.level > {};'.format(level))
    x = cur.fetchone()
    rank = x
    user = {
        'username': username,
        'level': level,
        'xp': xp,
        'rank': rank[0]+1
    }
    return {'user': user}

if __name__ == '__main__':
    app.run(debug=True, port=4500)