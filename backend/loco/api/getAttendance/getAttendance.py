from loco.api import api

@api.route('/getAttendance')
def getAttendance():
	"""
    	Returns attendance 
	
    	:returns: dictionary with the key and value of the attendance
    	"""
	return {'key' : 'value'}
