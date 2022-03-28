from loco.api import api

@api.route('/createGroup')
def createGroup():
	"""
    	Ensures group is created
	
    	:returns: dictionary with key and value of the group
    	"""
	return {'key' : 'value'}
