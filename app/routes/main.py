from flask import Blueprint, jsonify

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return jsonify({"message": "Hello, World!"})

@bp.app_errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Page not found"}), 404
