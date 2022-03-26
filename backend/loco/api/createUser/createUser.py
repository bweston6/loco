from loco.api import api

@api.route('/createUser')
def createUser():
	return {'key' : 'value'}
