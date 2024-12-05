from flask import Blueprint, jsonify, request
from ..db import query_db

bp = Blueprint('db', __name__)

@bp.route('/', methods=['GET'])
def index():
    try:
        query = "SELECT 1 + 1 AS result"
        result = query_db(query, one=True)
        message = f"Database connection successful." if result['result'] == 2 else "Database connection failed."
    except Exception as e:
        return jsonify({"error": "Database query failed", "details": str(e)}), 500
    return jsonify({"message": message})

@bp.route('/animals', methods=['GET'])
def animals():
    try:
        query = "SELECT * FROM animals"
        animals = query_db(query)
    except Exception as e:
        return jsonify({"error": "Failed to fetch animals", "details": str(e)}), 500
    return jsonify({"animals": animals})

@bp.route('/animals/<int:id>', methods=['GET'])
def animal(id):
    try:
        query = "SELECT * FROM animals WHERE id = %s"
        animal = query_db(query, (id,), one=True)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch animal with id {id}", "details": str(e)}), 500
    return jsonify({"animal": animal})

@bp.route('/animals/<string:diet>', methods=['GET'])
def diet(diet):
    try:
        query = "SELECT * FROM animals WHERE diet = %s"
        animals = query_db(query, (diet,))
    except Exception as e:
        return jsonify({"error": f"Failed to fetch animals with diet {diet}", "details": str(e)}), 500
    return jsonify({"animals": animals})

@bp.route('/animals', methods=['POST'])
def create_animal():
    try:
        name = request.json['name']
        habitat = request.json['habitat']
        diet = request.json['diet']
        query = "INSERT INTO animals (name, habitat, diet) VALUES (%s, %s, %s)"
        query_db(query, (name, habitat, diet), commit=True)
    except KeyError as e:
        return jsonify({"error": "Missing required fields", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to create animal", "details": str(e)}), 500
    return jsonify({"message": "Animal created"})

@bp.route('/animals/<int:id>', methods=['PUT'])
def update_animal(id):
    try:
        name = request.json['name']
        diet = request.json['diet']

        try:
            query = "SELECT * FROM animals WHERE id = %s"
            animal = query_db(query, (id,), one=True)
            if not animal:
                return jsonify({"error": f"Animal with id {id} not found"}), 404
        except Exception as e:
            raise

        query = "UPDATE animals SET name = %s, diet = %s WHERE id = %s"
        query_db(query, (name, diet, id), commit=True)
    except KeyError as e:
        return jsonify({"error": "Missing required fields", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to update animal with id {id}", "details": str(e)}), 500
    return jsonify({"message": f"Animal with id {id} updated"})

@bp.route('/animals/<int:id>', methods=['DELETE'])
def delete_animal(id):
    try:
        try:
            query = "SELECT * FROM animals WHERE id = %s"
            animal = query_db(query, (id,), one=True)
            if not animal:
                return jsonify({"error": f"Animal with id {id} not found"}), 404
        except Exception as e:
            raise
        query = "DELETE FROM animals WHERE id = %s"
        query_db(query, (id,), commit=True)
    except Exception as e:
        return jsonify({"error": f"Failed to delete animal with id {id}", "details": str(e)}), 500
    return jsonify({"message": f"Animal with id {id} deleted"})
