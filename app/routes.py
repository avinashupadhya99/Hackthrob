from app import app
from app.database import get_users, create_users
from flask import jsonify, request

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/users')
def users():
    users = get_users()

    return jsonify(users)

@app.route('/users/new', methods=['POST'])
def new_users():
    try:
        body = request.json
        print(body)
    except:
        msg = "payload must be a valid json"
        return jsonify({"error": msg}), 400

    try:
        new_user = create_users(body)
    except Exception as e:
        print(e)
        msg = "Internal error while creating new user"
        return jsonify({"error": msg}), 500
    return body