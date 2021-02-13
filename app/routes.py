from app import app
from app.database import get_users
from flask import jsonify

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/users')
def users():
    users = get_users()

    return jsonify(users)