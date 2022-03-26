from loco.api import api
import loco.database as db

@api.route('/createUser')
def createUser():
    conn = db.openConnection()
    if conn != None:
        db.createTables(conn.cursor())
        db.closeConnection(conn)
    else:
        return {'database' : 'error'}
    return {'key' : 'value'}
