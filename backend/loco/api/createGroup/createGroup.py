from loco.api import api

@api.route('/createGroup')
def createGroup():
	"""
    	Ensures group is created
	
    	:returns: dictionary with key and value of the group
    	"""
	return {'key' : 'value'}

#   "outline for the data insertion data can be of any type"
#   addGroup = ("INSERT INTO group "
#              "(group_id, group_name, emails) "
#              "VALUES (%s, %s, %s)")
#   dataGroup = (data, data, data)
#   cursor.execute(addGrouo, dataGroup)
#   conn.commit()