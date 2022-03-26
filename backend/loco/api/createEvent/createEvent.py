from loco.api import api

@api.route('/createEvent')
def createEvent():
	return {'key' : 'value'}
