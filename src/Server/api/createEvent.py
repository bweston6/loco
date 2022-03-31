# being worked on by Noushin

from . import api

@api.route('/createEvent')
def createEvent():
	"""
    	Ensures event is created
	
    	:returns: dictionary with the key and value of the event
    	"""
	return {'key' : 'value'}

#   "outline for the data insertion data can be of any type"
#   addEvents = ("INSERT INTO events "
#              "(event_ID, event_name, start_time, duration, latitude, longitude, radius, description, emails) "
#              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
#   dataEvents = (data, data, data, data, data, data, data, data, data)
#   cursor.execute(addUser, dataUser)
#   conn.commit()
