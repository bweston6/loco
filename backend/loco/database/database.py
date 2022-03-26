from mysql.connector import connect, Error, errorcode

try:
    conn = connect(
            host = "localhost",
            user = "loco",
            unix_socket = "/var/lib/mysql/mysql.sock")
    cursor = conn.cursor()
except Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Incorrect username or password")
    else:
        print(err)
    exit(1)

DATABASE = 'loco'
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

def createDatabase(cursor):
    try:
        cursor.execute("USE {}".format(DATABASE))
    except Error as err:
        print("Database {} does not exist.".format(DATABASE))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            try:
                cursor.execute("CREATE DATABASE {}".format(DATABASE))
            except Error as err:
                print("Database creation failed: {}".format(err))
                exit(1)
            print("Database {} successfully created".format(DATABASE))
            conn.database = DATABASE
        else:
            print(err)
            exit(1)

def createTables(cursor):
    for tableName in TABLES:
        tableDescription = TABLES[tableName]
        try:
            print("creating table {}: ".format(tableName), end='')
            cursor.execute(tableDescription)
        except Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("created.")

def main():
    createDatabase(cursor)
    createTables(cursor)

main()
cursor.close()
conn.close()