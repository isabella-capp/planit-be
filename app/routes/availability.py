from flask import (Blueprint, request, jsonify)

from app.db import query_db

bp = Blueprint('availability', __name__, url_prefix='/api')

def formatted_data(availability_data): 
    formatted_data = []
    for entry in availability_data:
        date = entry[0].strftime('%Y-%m-%d')  # Format date as 'YYYY-MM-DD'
        start_time = entry[1].strftime('%H:%M')  # Format start time as 'HH:MM'
        end_time = entry[2].strftime('%H:%M')  # Format end time as 'HH:MM'
        formatted_data.append({
            "date": date,
            "start_time": start_time,
            "end_time": end_time
        })
    print("Formatted data:", formatted_data)
    return formatted_data

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
        formatted_data = formatted_data(availability_data)
        print("Formatted data:", formatted_data)
        # Format the response data
        if formatted_data:
            return jsonify(formatted_data), 200
        else:
            return jsonify([]), 200  # Return an empty list if no data found

    except Exception as e:
        return jsonify({"error": "Failed to fetch availability", "details": str(e)}), 500
    

@bp.route('/api/get_group_availability', methods=['POST'])
def get_group_availability():
    data = request.get_json()
    event_id = data.get("eventId")

    if not event_id:
        return jsonify({"error": "Missing event ID"}), 400

    try:
        query = """
            SELECT date, start_time, end_time, COUNT(*) AS num_users
            FROM availability
            WHERE event_id = ?
            GROUP BY date, start_time, end_time
            ORDER BY date, start_time;
        """
        availability_data = query_db(query, (event_id,))

        for row in availability_data:
            date = row["date"]
            time_slot = row["start_time"]  # Considero solo start_time per le celle della tabella
            count = row["num_users"]

            if date not in availability_data:
                availability_data[date] = {}
            
            availability_data[date][time_slot] = count

        return jsonify({"availability": availability_data})
    except Exception as e:
        return jsonify({"error": "Failed to fetch availability", "details": str(e)}), 500