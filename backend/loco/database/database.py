from mysql.connector import connect, Error, errorcode

TABLES = {}
TABLES['users'] = (
        "CREATE TABLE `users` ("
        "  `full_name` varchar(100) NOT NULL,"
        "  `email` varchar(100) NOT NULL,"
        "  `hostFlag` BIT NOT NULL,"
        "  CONSTRAINT PRIMARY KEY (`email`)"
        ")")

TABLES['events'] = (
        "CREATE TABLE `events` ("
        "  `event_ID` int NOT NULL,"
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
        "  `group_ID` int NOT NULL,"
        "  `group_name` varchar(50) NOT NULL,"
        "  `emails` JSON NOT NULL,"
        "  CONSTRAINT PRIMARY KEY (`group_ID`)"
        ")")

def openConnection():
    try:
        conn = connect(
                host = "localhost",
                unix_socket = "/var/lib/mysql/mysql.sock",
                user = "loco",
                database = "loco")
        return conn
    except Error
        return None

def createTables(cursor):
    for tableName in TABLES:
        tableDescription = TABLES[tableName]
        try:
            print("creating table {}: ".format(tableName), end='')
            cursor.execute(tableDescription)
        except Error as e:
            if e.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                return True
            else:
                return True
        else:
            return True

def closeConnection(conn):
    conn.cursor.close()
    conn.close()
