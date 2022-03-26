from loco.api import api

@api.route('/getEvent')
def getEvent():
	return {'key' : 'value'}
