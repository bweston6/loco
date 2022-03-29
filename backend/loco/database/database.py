from mariadb import connect, Error
from mysql.connector import errorcode

TABLES = {}
TABLES['users'] = (
        "CREATE TABLE `users` ("
        "  `full_name` varchar(100) NOT NULL,"
        "  `email` varchar(100) NOT NULL,"
        "  `auth` varchar(100) NOT NULL,"
        "  `host_flag` BIT NOT NULL,"
        "  CONSTRAINT PRIMARY KEY (`email`)"
        ")")

TABLES['events'] = (
        "CREATE TABLE `events` ("
        "  `event_ID` int NOT NULL AUTO_INCREMENT,"
        "  `event_name` varchar(50) NOT NULL,"
        "  `start_time` datetime NOT NULL,"
        "  `duration` time NOT NULL,"
        "  `latitude` decimal(8,6) NOT NULL,"
        "  `longitude` decimal(9,6) NOT NULL,"
        "  `radius` int NOT NULL,"
        "  `description` varchar(1000),"
        "  `emails` JSON NOT NULL,"
        "  CONSTRAINT PRIMARY KEY (`event_ID`)"
        ")")

TABLES['groups'] = (
        "CREATE TABLE `groups` ("
        "  `group_ID` int NOT NULL AUTO_INCREMENT,"
        "  `group_name` varchar(50) NOT NULL,"
        "  `emails` JSON NOT NULL,"
        "  CONSTRAINT PRIMARY KEY (`group_ID`)"
        ")")

def openConnection():
    """
    Description
    
    :returns: 
    """
    conn = connect(
            unix_socket = "/run/mysqld/mysqld.sock",
            database = "loco")
    return conn

def createTables(cursor):
    """
    Description
    
    :param: 
    :raise: 
    :returns: 
    """
    for tableName in TABLES:
        tableDescription = TABLES[tableName]
        try:
            print("creating table {}: ".format(tableName), end='')
            cursor.execute(tableDescription)
        except Error as e:
            if e.errno != errorcode.ER_TABLE_EXISTS_ERROR:
                raise e
    return True

def closeConnection(conn):
    """
    Description
    
    :param: 
    :returns: 
    """
    conn.close()
    return True
