# being worked on by timi


from . import api
from flask import jsonify, request
from mariadb import Error
import logging, 
from .. import auth, database as db



@api.route('/getEvent')
def getEvent():
	"""Gets event from database
	
    	:<json number eventId: The event id.
    	:<json string eventName: The event name that you want to get.
    	:<json number startTime: The starting time of the event, after the attendance has been taken
	:<json number duration: The duration of an event.
	:<json number locationLong: The longitute coordinate of an event's location.
	:<json number locationLat: The latitude coordinate of an event's location.
	:<json number radius: The radius around an event's coordinates where attendance is accepted.
	:<json string description: Get a description of the event for users.
	:<json string email: A list of emails signed up that are expected to attend the event.
	
	:>json string error: An error message if the action cannot complete

	:statuscode 200: Operation completed successfully
    	:statuscode 400: JSON parameters are missing
    	:statuscode 500: Server database error
	
    	:returns: dictionary with the key and value of the event
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
            	    'emails' in requestData):
			
			
		    query = ("""SELECT *
                    FROM events
                    WHERE eventId = ?
          	    """)
		
		    conn = db.openConnection()
            	    cursor = conn.cursor()
		    cursor.execute(query, (requestData['eventId'], ))
                    
		    event = cursor.fetchone()
                    event = {"eventId": event[0],
                        "eventName": event[1],
                        "startTime": event[2],
			"duration": event[3],
			"locationLong": event[4],
			"locationLat": event[5],
			"radius": event[6],
			"description": event[7],
			"emails": event[8],)
                        }
                    return jsonify(user), 200
		
		else:
            	    return jsonify(error='missing parameters'), 400
	
	
	except Error as e:
            logging.error(e)
            return jsonify(error='database error'), 500
