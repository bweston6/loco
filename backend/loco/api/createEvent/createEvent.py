from loco.api import api

@api.route('/createEvent')
def createEvent():
	"""
    	Ensures event is created
    	:returns: the key and value of the event
	:rtype: dictionary
    	"""
	return {'key' : 'value'}
