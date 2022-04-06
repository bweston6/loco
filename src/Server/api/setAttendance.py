#Gunan
#incomplete still

from . import api
from .. import auth, database as db
from flask import jsonify, request
from mariadb import Error
import logging

@api.route('/setAttendance')
def setAttendance():
	"""
    	Ensures attendance is set
	
    	:returns: dictionary with the key and value of the attendance
    	"""
    try:
        requestData = request.get_json()
        if ('token' in requestData and 'email' in requestData and 'eventID' in requestData):
            q1 = (""" UPDATE user
                SET attendance = "True"
                WHERE eventID = ?
            """)
            conn = db.openConnection()
            cursor = conn.cursor()
            cursor.execute(q1, (requestData['EventID'], ))
        
        else:
            return jsonify(error='missing parameters'), 400      
    
    except Error as e:
        logging.error(e)
        return jsonify(error='database error'), 500
