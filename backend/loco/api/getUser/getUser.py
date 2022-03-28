from loco.api import api

@api.route('/getUser')
def getUser():
	"""
    	Returns the user
	
    	:returns: dictionary with the key and value of the user
    	"""
	return {'key' : 'value'}
