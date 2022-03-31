from . import api

@api.route('/getEvent')
def getEvent():
	"""
    	Returns the event
	
    	:returns: dictionary with the key and value of the event
    	"""
	return {'key' : 'value'}
