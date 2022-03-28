from loco.api import api

@api.route('/createGroup')
def createGroup():
	"""
    	Ensures group is created
    	:returns: the key and value of the group
	:rtype: dictionary
    	"""
	return {'key' : 'value'}
