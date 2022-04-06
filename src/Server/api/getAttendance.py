#Gunan
#mans on it still

from . import api
from .. import auth, database as db
from flask import jsonify, request
from mariadb import Error
import logging

@api.route('/getAttendance')
def getAttendance():
	"""
    	Returns attendance 
	
    	:returns: dictionary with the key and value of the attendance
    	"""
    try:
        requestData = request.get_json()
        if ('token' in requestData and 'email' in requestData and 'eventID' in requestData):
            q1 = (""" SELECT attendance 
                FROM Users
                WHERE token = ?
            """)
            conn = db.openConnection()
            cursor = conn.cursor()
            cursor.execute(q1, (requestData['token'], ))
            attendance = cursor.fetchone()[0]
            
            return attendance
        
        else:
            return jsonify(error='missing parameters'), 400      
    
    except Error as e:
        logging.error(e)
        return jsonify(error='database error'), 500
