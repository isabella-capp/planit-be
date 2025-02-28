from flask import Blueprint, request, jsonify, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import query_db

bp = Blueprint('auth', __name__, url_prefix='/api')

def _get_user(username):
    """Helper function to retrieve user by username."""
    try:
        query = "SELECT * FROM users WHERE username = %s"
        return query_db(query, (username,), one=True)
    except Exception as e:
        return None
    
def _check_email(email):
    """Helper function to retrieve user by username."""
    try:
        query = "SELECT * FROM users WHERE email = %s"
        return query_db(query, (email,), one=True)
    except Exception as e:
        return None

@bp.route('/signin', methods=['POST'])
def signin():
    if not request.is_json:
        return jsonify({"error": "Invalid request format"}), 400

    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = _get_user(username)

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({"message": "Invalid username or password", "status": "error"}), 401

    session.clear()
    session.permanent = True
    session['username'] = user['username']
    session['id'] = user['id']

    return jsonify({"message": "Login successful!"}), 200

@bp.route('/signup', methods=['POST'])
def signup():
    if not request.is_json:
        return jsonify({"error": "Invalid request format"}), 400

    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if _get_user(username):
        return jsonify({"message": "Username already exists", "status": "error"}), 400

    if _check_email(email):
        return jsonify({"message": "Email already exists", "status": "error"}), 400
    
    try:
        hashed_password = generate_password_hash(password)
        query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
        query_db(query, (username, email, hashed_password), commit=True)
    except Exception as e:
        current_app.logger.error(f"Failed to create user: {e}")
        return jsonify({"error": "Failed to create user", "details": str(e)}), 500

    return jsonify({"message": "Signup successful!"}), 201

@bp.route('/user', methods=['GET'])
def get_logged_in_user():
    username = session.get('username')
    id = session.get('id')
    print('Session data in /user:', dict(session))
    
    if username is None:
        return jsonify({"message": "No user logged in", "status": "error"}), 401
    
    return jsonify({'username': username, 'id': id}), 200

@bp.route('/check-session', methods=['GET'])
def check_session():
    if 'username' in session:
        return jsonify({"status": "authenticated", "user": session['username']}), 200
    else:
        return jsonify({"status": "unauthenticated"}), 401

@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logout successful!"}), 200