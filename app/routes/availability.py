from datetime import datetime
from flask import (Blueprint, request, jsonify)

from app.db import query_db

bp = Blueprint('availability', __name__, url_prefix='/api')

def get_username(user_id):
    query = "SELECT username FROM users WHERE id = %s;"
    result = query_db(query, (user_id,), one=True)
    return result.get("username") if result else None

@bp.route('/availability', methods=['POST'])
def save_availability():
    data = request.get_json()
    user_id = data.get("user_id")
    event_id = data.get("event_id")
    slots = data.get("slots", [])

    print("Data:", data)
    if not user_id or not event_id or not slots:
        return jsonify({"error": "Dati mancanti"}), 400
    
    try:
        for slot in slots:
            date = slot.get("date")
            start_time = slot.get("start_time")
            end_time = slot.get("end_time")

            print("Slot data:", date, start_time, end_time)
            # Check if the slot data is complete
            if not date or not start_time or not end_time:
                return jsonify({"error": "Slot data incomplete"}), 400

            query = """
                INSERT INTO availability (user_id, event_id, date, start_time, end_time) 
                VALUES (%s, %s, %s, %s, %s);
            """
            query_db(query, (user_id, event_id, date, start_time, end_time), commit=True)

    except Exception as e:
        return jsonify({"error": "Failed to save availability", "details": str(e)}), 500

    return jsonify({"message": "Disponibilità salvata con successo!"}), 200


@bp.route('/get_availability', methods=['POST'])
def get_availability():
    data = request.get_json()
    user_id = data.get('user_id')
    event_id = data.get('event_id')

    print("Data get:", data)

    if not user_id or not event_id:
        return jsonify({"error": "user_id and event_id are required"}), 400

    try:
        query = """
            SELECT date, start_time, end_time 
            FROM availability 
            WHERE user_id = %s AND event_id = %s;
        """
        availability_data = query_db(query, (user_id, event_id))
        print("Availability data:", availability_data)
    
        # Format the response data
        if availability_data:
            return jsonify(availability_data), 200
        else:
            return jsonify([]), 200  # Return an empty list if no data found

    except Exception as e:
        return jsonify({"error": "Failed to fetch availability", "details": str(e)}), 500
    

@bp.route('/get_group_availability', methods=['POST'])
def get_group_availability():
    data = request.get_json()
    event_id = data.get("eventId")

    if not event_id:
        return jsonify({"error": "Missing event ID"}), 400

    try:
        query = """
            SELECT date, start_time, user_id 
            FROM availability 
            WHERE event_id = %s;
        """
        availability_data = query_db(query, (event_id,))

        group_availability = {}

        for row in availability_data:
            date = row["date"]
            time_slot = row["start_time"]
            user_id = row["user_id"]  # Ensure this field exists in your table
            
            username = get_username(user_id)  # Get the username using the user_id

            if username:  # Only proceed if a username is found
                if date not in group_availability:
                    group_availability[date] = {}
                if time_slot not in group_availability[date]:
                    group_availability[date][time_slot] = []
                
                group_availability[date][time_slot].append(username)

        print("Group availability:", group_availability)

        return jsonify({"availability": group_availability})
    except Exception as e:
        print(f"Error fetching availability: {str(e)}")
        return jsonify({"error": "Failed to fetch availability", "details": str(e)}), 500
