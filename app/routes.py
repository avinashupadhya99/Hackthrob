from app import app
import json
from app.database import create_users, get_skills, get_users, get_user_by_id
from flask import jsonify, request

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/users')
def users():
    users = get_users()

    return jsonify([i.serialize for i in users])

@app.route('/skills')
def skills():
    skills = get_skills()

    return jsonify([i.serialize for i in skills])

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

@app.route('/user/<int:id>')
def get_user(id):
    user = get_user_by_id(id)
    return jsonify(user.serialize)

@app.route('/getmatch')
def get_match():
    user_id = request.args.get('user_id')
    return user_id