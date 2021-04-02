from flask import Flask
app = Flask(__name__)

@app.route('/auth/login', methods=['POST'])
def auth_login():
    return {}

@app.route('/auth/register', methods=['POST'])
def auth_register():
    return {}

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