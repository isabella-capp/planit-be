from datetime import timedelta
import random
from flask import (Blueprint, request, jsonify, current_app)

from app.db import query_db

bp = Blueprint('dashboard', __name__, url_prefix='/private')


@bp.route('/create_event', methods=['POST'])
def create_event():
    if not request.is_json:
            return jsonify({"error": "Invalid request format"}), 400
    data = request.json

    event_name = data.get('name')
    start_time = data.get('startTime')
    end_time = data.get('endTime')
    dates = data.get('datesJSON')

    event_id = random.randint(100000, 999999)

    print("Event data:", event_name, start_time, end_time, dates)

    try:
        query = "INSERT INTO events (id, name, start_time, end_time, dates) VALUES (%s, %s, %s, %s, %s);"
        query_db(query, (event_id, event_name, start_time, end_time, dates,), commit=True)
    except Exception as e:
        return jsonify({"error": "Failed to create an event", "details": str(e)}), 500

    return jsonify({"message": "Event created successfully!", "event_id": event_id}), 200

def convert_seconds_to_time(seconds):
    time = str(timedelta(seconds=seconds))
    time = time.split(" ")[-1][:5]
    if time.endswith(":"):
        time = time[:-1]
    return time

def serialize_event(event):
    for key, value in event.items():
        if isinstance(value, timedelta):
            event[key] = convert_seconds_to_time(value.total_seconds())
    return event

@bp.route('/dashboard/<int:id>', methods=['GET'])
def get_event(id):
    try:
        query = "SELECT * FROM events WHERE id = %s"
        event = query_db(query, (id,), one=True)
        serialized_event = serialize_event(event)
        print("evento serializzato:", serialized_event)
    except Exception as e:
        current_app.logger.error(f"Failed to fetch event with id {id}: {e}")
        return jsonify({"error": f"Failed to fetch event with id {id}", "details": str(e)}), 500
    return jsonify({"event": serialized_event})