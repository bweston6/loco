# being worked on by timi


from . import api
from flask import jsonify, request
from mariadb import Error
import logging, 
from .. import auth, database as db



@api.route('/getEvent')
def getEvent():
	"""Gets event from database
	
    	Returns the event
	
    	:returns: dictionary with the key and value of the event
    	"""
	return {'key' : 'value'}
