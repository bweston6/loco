import Server.database as db

def test_createAttendance(conn):
    cursor = conn.cursor()
    showSchema = ("DESCRIBE loco.attendance")
    cursor.execute(showSchema)
    schema = cursor.fetchall()
    email = schema[0]; event_ID = schema[1]; attendance_flag = schema[2]
    assert ("email", "varchar(100)", "NO", "PRI", None, "") == email
    assert ("event_ID", "int", "NO", "PRI", None, "") == event_ID
    assert ("attendance_flag", "tinyint(1)", "NO", "", None, "") == attendance_flag

def test_createEvents(conn):
    cursor = conn.cursor()
    showSchema = ("DESCRIBE loco.events")
    cursor.execute(showSchema)
    schema = cursor.fetchall()
    assert ('event_ID', 'int', 'NO', 'PRI', None, 'auto_increment') == schema[0]
    assert ('event_name', 'varchar(50)', 'NO', '', None, '') == schema[1]
    assert ('start_time', 'bigint', 'NO', '', None, '') == schema[2]
    assert ('duration', 'bigint', 'NO', '', None, '') == schema[3]
    assert ('latitude', 'decimal(8,6)', 'NO', '', None, '') == schema[4]
    assert ('longitude', 'decimal(9,6)', 'NO', '', None, '') == schema[5]
    assert ('radius', 'int', 'NO', '', None, '') == schema[6]
    assert ('description', 'varchar(1000)', 'YES', '', None, '') == schema[7]
    assert ('hostEmail', 'varchar(100)', 'NO', 'MUL', None, '') == schema[8]

def test_createGroups(conn):
    cursor = conn.cursor()
    showSchema = ("DESCRIBE loco.groups")
    cursor.execute(showSchema)
    schema = cursor.fetchall()
    assert ('group_ID', 'int', 'NO', 'PRI', None, 'auto_increment') == schema[0]
    assert ('group_name', 'varchar(50)', 'NO', '', None, '') == schema[1]
    assert ('hostEmail', 'varchar(100)', 'NO', 'MUL', None, '') == schema[2]
    assert ('emails', 'json', 'NO', '', None, '') == schema[3]

def test_createUsers(conn):
    cursor = conn.cursor()
    showSchema = ("DESCRIBE loco.users")
    cursor.execute(showSchema)
    schema = cursor.fetchall()
    assert ('full_name', 'varchar(100)', 'NO', '', None, '') == schema[0]
    assert ('email', 'varchar(100)', 'NO', 'PRI', None, '') == schema[1]
    assert ('token', 'varchar(1000)', 'NO', '', None, '') == schema[2]
    assert ('host_flag', 'tinyint(1)', 'NO', '', None, '') == schema[3]