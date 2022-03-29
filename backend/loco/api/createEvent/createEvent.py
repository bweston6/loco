# being worked on by Noushin
from loco.api import api

@api.route('/createEvent')
def createEvent():
	"""
    	Ensures event is created
	
    	:returns: dictionary with the key and value of the event
    	"""
	return {'key' : 'value'}
