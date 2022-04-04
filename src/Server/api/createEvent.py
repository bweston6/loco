# being worked on by Noushin

from flask import jsonify, request
from mariadb import Error
from . import api
from .. import auth, database as db
import logging

@api.route('/createEvent')
def createEvent():
    """Creates an event and adds the information to the database.

    :<json number eventId: The event id.
    :<json string eventName: The event name.
    :<json number startTime: The time the event is expected to start, after which attendance will be marked.
    :<json number duration: The duration of an event.
    :<json number locationLong: The longitute coordinate of an event's location.
    :<json number locationLat: The latitude coordinate of an event's location.
    :<json number radius: The radius around an event's coordinates where attendance is accepted.
    :<json string description: A description of the event for users.
    :<json string email: A list of emails signed up that are expected to attend the event.

    :>json string error: An error message if the action cannot complete

    :statuscode 200: Operation completed successfully
    :statuscode 400: JSON parameters are missing
    :statuscode 500: Server database error
    """
    try:
        requestData = request.get_json()
        if ('eventId' in requestData and 
            'eventName' in requestData and
            'startTime' in requestData and
            'duration' in requestData and
            'locationLong' in requestData and
            'locationLat' in requestData and
            'radius' in requestData and
            'description' in requestData and
            'email' in requestData
        ):
            conn = db.openConnection()
            cursor = conn.cursor()
            addEvent = ("""REPLACE INTO events (
                    event_ID, 
                    event_name, 
                    start_time, 
                    duration, 
                    latitude,
                    longitude,
                    radius,
                    description,
                    emails
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            )
            eventData = (
                requestData['eventId'],
                requestData['eventName'],
                requestData['startTime'],
                requestData['duration'],
                requestData['locationLat'],
                requestData['locationLong'],
                requestData['radius'],
                requestData['description'],
                requestData['email']
            )
            cursor.execute(addEvent, eventData)
            conn.commit()
            db.closeConnection(conn)
            return jsonify(eventData), 200
        else: 
            return jsonify(error='missing parameters'), 400
    except Error as e:
        logging.error(e)
        return jsonify(error='database error'), 500
