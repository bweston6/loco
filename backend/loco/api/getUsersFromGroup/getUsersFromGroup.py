from loco.api import api

@api.route('/getUsersFromGroup')
def getUsersFromGroup():
	"""
    	Returns the users from the selected group
	
    	:returns: dictionary with the key and value of the user from a specific group
    	"""
	return {'key' : 'value'}
