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
    user_id = session.get("id")
    print(user_id)
    print("Event data:", event_name, start_time, end_time, dates)

    try:
        query = "INSERT INTO events (id, user_id, name, start_time, end_time, dates) VALUES (%s, %s, %s, %s, %s, %s);"
        query_db(query, (event_id, user_id, event_name, start_time, end_time, dates,), commit=True)
    except Exception as e:
        print("query fallita")
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

@bp.route('/user/admin/event')
def get_event_where_user_is_admin():
    user_id = session.get('id')

    if not user_id:
        return jsonify({"error": "User not in Session"}), 400
    
    try:
        query = """
            SELECT * FROM events e
            WHERE e.user_id = %s;
        """
        events = query_db(query, (user_id,))
        events = events_with_partecipants(events)   
    except Exception as e:
        return jsonify({"error": "Failed to fetch event", "details": str(e)}), 500
    
    return jsonify({"events": events}), 200    

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

def events_with_partecipants(events):
    for event in events:
        event_id = event.get('id')
        partecipants = number_of_partecipants_for_event(event_id)
        print(partecipants)
        event['partecipants'] = partecipants
    return events

def number_of_partecipants_for_event(event_id):
    if not event_id:
        print("No event ID provided")
        return 0  

    try:
        query = """
            SELECT COUNT(DISTINCT user_id) AS partecipants
            FROM availability
            WHERE event_id = %s;
        """
        result = query_db(query, (event_id,))
        partecipants = result[0]['partecipants'] if result else 0
    except Exception as e:
        print(f"Error fetching participants: {str(e)}")
        return 0  

    return partecipants

def add_info_to_closed_events(results):
    try:
        for result in results:
            event_id = result.get('id')
            closed_event_info = get_closed_event_info(event_id)
            print("Closed event info:", closed_event_info)
            is_completed = closed_event_info.get('is_completed')
            print("is_completed:", is_completed)

            # Add the closed event information to the result
            result['is_completed'] = closed_event_info.get('is_completed')
            result['final_date'] = closed_event_info.get('final_date')
            result['final_time'] = closed_event_info.get('final_time')
            
    except Exception as e:
        print(f"Error processing closed events: {str(e)}")

    return results

def get_closed_event_info(event_id):
    try:
        query = """
            SELECT event_date, event_time
            FROM closed_events
            WHERE event_id = %s;
        """
        closed_event = query_db(query, (event_id,), one=True)  # Get a single result

        if closed_event:
            return {
                "is_completed": True,
                "final_date": closed_event['event_date'],
                "final_time": closed_event['event_time']
            }
        else:
            return {
                "is_completed": False,
                "final_date": None,
                "final_time": None
            }
    except Exception as e:
        print(f"Error fetching closed event info: {str(e)}")
        return {
            "is_completed": False,
            "final_date": None,
            "final_time": None
        }

@bp.route('/user/results/<int:user_id>', methods=['GET'])
def get_results(user_id):
    print("User ID:", user_id)
    try:
        query = """
            SELECT 
            e.id AS id, 
            e.name AS event_name
            FROM events e
            JOIN availability a ON e.id = a.event_id
            WHERE a.user_id = %s
            GROUP BY e.id, e.name;
        """

        results = query_db(query, (user_id,))
        print("query:", results)
        results = events_with_partecipants(results)
        print("with partecipants", results)
        results = add_info_to_closed_events(results)
        print(results)
    except Exception as e:
        return jsonify({"error": "Failed to fetch results", "details": str(e)}), 500

    return jsonify({"results": results}), 200