from loco.api import api

@api.route('/getUser')
def getUser():
	return {'key' : 'value'}
