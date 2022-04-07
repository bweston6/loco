# being worked on by timi

from . import api
from .. import auth, database as db
from flask import jsonify, request
from mariadb import Error
import logging, jwt



@api.route('/getEvent' , methods=['POST'] )
def getEvent():
    """Gets event from database

    :<json number eventId: The event id.
    :<json str token: A valid authentication token (see :http:post:`/api/createUser`)

    :>json string error: An error message if the action cannot complete

    :statuscode 200: Operation completed successfully
    :statuscode 400: JSON parameters are missing
	:statuscode 401: Invalid authentication token
    :statuscode 500: Server database error
    """
    try:
        requestData = request.get_json()
        if ('eventId' in requestData and 
                'token' in requestData):
            
			# validation of token
			query1 = ("""SELECT EXISTS (
                SELECT *
                FROM events
                WHERE token = ?
                LIMIT 1
            )
            """)
			
			query2 = ("""SELECT *
                    FROM events
                    WHERE eventId = ?
                """)
            conn = db.openConnection()
            cursor = conn.cursor()
            cursor.execute(query1, (requestData['token'], ))
            tokenValid = cursor.fetchone()[0]
			
			if tokenValid == 1:
                cursor.execute(query2, (requestData['eventId'], ))
                event = cursor.fetchone()
                event = {"eventId": event[0],
                        }
                return jsonify(event), 200
            
			else:
                db.closeConnection(conn)
                raise jwt.InvalidTokenError
			
        else:
            return jsonify(error='missing parameters'), 400
    
	except jwt.InvalidTokenError as e:
        logging.info('User query attempted with invalid token')
        return jsonify(error='invalid token'), 401
	except Error as e:
        logging.error(e)
        return jsonify(error='database error'), 500
