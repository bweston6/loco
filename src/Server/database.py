from mariadb import connect

TABLES = {}
TABLES["users"] = (
    "CREATE TABLE `users` ("
    "  `full_name` varchar(100) NOT NULL,"
    "  `email` varchar(100) NOT NULL,"
    "  `token` varchar(1000) NOT NULL,"
    "  `host_flag` BOOLEAN NOT NULL,"
    "  CONSTRAINT PRIMARY KEY (`email`)"
    ")"
)

TABLES["events"] = (
    "CREATE TABLE `events` ("
    "  `event_ID` int NOT NULL AUTO_INCREMENT,"
    "  `event_name` varchar(50) NOT NULL,"
    "  `start_time` bigint NOT NULL,"
    "  `duration` bigint NOT NULL,"
    "  `latitude` decimal(8,6) NOT NULL,"
    "  `longitude` decimal(9,6) NOT NULL,"
    "  `radius` int NOT NULL,"
    "  `description` varchar(1000),"
    "  `hostEmail` varchar(100) NOT NULL,"
    "  CONSTRAINT FK_Events FOREIGN KEY (hostEmail) REFERENCES users(email),"
    "  CONSTRAINT PRIMARY KEY (`event_ID`)"
    ")"
)

TABLES["groups"] = (
    "CREATE TABLE `groups` ("
    "  `group_ID` int NOT NULL AUTO_INCREMENT,"
    "  `group_name` varchar(50) NOT NULL,"
    "  `hostEmail` varchar(100) NOT NULL,"
    "  `emails` JSON NOT NULL,"
    "  CONSTRAINT PRIMARY KEY (`group_ID`),"
    "  CONSTRAINT FK_Groups FOREIGN KEY (hostEmail) REFERENCES users(email)"
    ")"
)

TABLES["attendance"] = (
    "CREATE TABLE `attendance` ("
    "  `email` varchar(100) NOT NULL,"
    "  `event_ID` int NOT NULL,"
    "  `attendance_flag` BOOLEAN NOT NULL,"
    "  CONSTRAINT PK_attendance PRIMARY KEY(email, event_ID),"
    "  CONSTRAINT FK_attendance_event_ID FOREIGN KEY (event_ID) REFERENCES events(event_ID)"
    ")"
)


def openConnection():
    """Opens a connection to the ``loco`` database using a Unix socket.

    :rasies mariadb.Error: If there is an error connecting to the database
    :return: The connection to the database
    :rtype: mariadb.connection
    """
    conn = connect(unix_socket="/var/run/mysqld/mysqld.sock", database="loco")
    return conn


def createTables(cursor):
    """Creates the tables defined in the dictionary ``TABLES``. If the tables exist then there is no change to the database.

    :param cursor: A ``cursor`` in the database you want to write to
    :type cursor: mariadb.connection.cursor
    :raises mariadb.Error: If there is an error writing to the database
    :return: True if the function is successful
    :rtype: bool
    """
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    for tableName in TABLES:
        dropTable = "DROP TABLE IF EXISTS " + tableName
        tableDescription = TABLES[tableName]
        # todo - remove me after table schema are finalised
        cursor.execute(dropTable)
        cursor.execute(tableDescription)
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    return True


def closeConnection(conn):
    """Closes an open database connection object.

    :param conn: The connection you want to close
    :type conn: mariadb.connection
    :raises mariadb.Error: If there is no connection to close
    :return: True when the action is complete
    :rtype: bool
    """
    conn.close()
    return True
