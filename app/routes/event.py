from datetime import timedelta
import random
from flask import (Blueprint, request, jsonify, session)
from functools import wraps
from app.db import query_db

bp = Blueprint('dashboard', __name__, url_prefix='/private')

@bp.route('/create_event', methods=['POST'])
def create_event():
    if not request.is_json:
            return jsonify({"error": "Invalid request format"}), 400
    data = request.json

    event_name = data.get('name')
    selectedTimes = data.get('selectedTimes')
    dates = data.get('datesJSON')
    start_time = selectedTimes.get('startTime')
    end_time = selectedTimes.get('endTime')
    event_id = random.randint(100000, 999999)

    print("Event data:", event_name, start_time, end_time, dates)

    try:
        query = "INSERT INTO events (id, name, start_time, end_time, dates) VALUES (%s, %s, %s, %s, %s);"
        query_db(query, (event_id, event_name, start_time, end_time, dates,), commit=True)
    except Exception as e:
        return jsonify({"error": "Failed to create an event", "details": str(e)}), 500

    return jsonify({"message": "Event created successfully!", "event_id": event_id}), 200

@bp.route('/event/<int:id>', methods=['GET'])
def get_event(id):
    try:
        query = "SELECT * FROM events WHERE id = %s"
        event = query_db(query, (id,), one=True)
        print("Evento:", event)

        if not event:
            return jsonify({"error": f"Event with id {id} not found"}), 404
        
    except Exception as e:
        return jsonify({"error": f"Failed to fetch event with id {id}", "details": str(e)}), 500
    return jsonify({"event": event}), 200

@bp.route('/user/events', methods=['POST'])
def get_user_events():
    data = request.get_json()
    user_id = data.get('userId')

    if not data:
        return jsonify({"error": "No data received"}), 400
    
    print("User ID:", user_id)

    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400

    try:
        query = """
           SELECT e.id AS event_id, 
            e.name AS event_name, 
            e.start_time AS event_start_time, 
            e.end_time AS event_end_time, 
            e.dates AS event_dates
            FROM events e
            JOIN availability a ON e.id = a.event_id
            WHERE a.user_id = %s
            GROUP BY e.id, e.name, e.start_time, e.end_time, e.dates;
        """
                
        events = query_db(query, (user_id,))

        print(events)
    except Exception as e:
        return jsonify({"error": "Failed to fetch events", "details": str(e)}), 500

    return jsonify({"events": events}), 200