from loco.api import api

@api.route('/setAttendance')
def setAttendance():
	"""
    	Ensures attendance is set
	
    	:returns: dictionary with the key and value of the attendance
    	"""
	return {'key' : 'value'}
