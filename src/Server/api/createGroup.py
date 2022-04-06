# being worked on by Leon

from . import api
from .. import auth, database as db
from flask import jsonify, request
from mariadb import Error
import logging

@api.route('/createGroup', methods=['POST'])
def createGroup():
    """Creates a group with a set of emails to allow for quicker repeating event creation

    :<json int groupID: The groups unique ID
    :<json string groupName: The groups name
    :<json string[] emails: All the users emails that are in the group

    :>json string error: An error message if the action cannot complete

    :statuscode 200: Operation completed successfully
    :statuscode 400: JSON parameters are missing
    :statuscode 500: Server database error
    """
    try:
        requestData = request.get_json()
        if ('groupID' in requestData and 'groupName' in requestData and 'emails' in requestData):
            conn = db.openConnection()
            cursor = conn.cursor()
            addGroup = ("""REPLACE INTO group (
                    group_id, 
                    group_name, 
                    emails
                ) 
                VALUES (?, ?, ?)"""
            )
            groupData = (
            requestData['groupID'],
            requestData['groupName'],
            requestData['emails']
            )
            cursor.execute(addGroup, groupData)
            conn.commit()
            db.closeConnection(conn)
            return jsonify(groupData), 200
        else: 
            return jsonify(error='missing parameters'), 400
    except Error as e:
        logging.error(e)
        return jsonify(error='database error'), 500
