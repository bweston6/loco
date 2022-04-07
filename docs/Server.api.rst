.. _Server.api:

Server.api package
==================
This section details all of the API endpoints that are available.

To make a manual request to the API you first need to receive an authentication token:

#. Authenticate you email address using: :http:post:`/api/authenticateEmail`:
    
    .. code-block:: bash

        $ curl -i -X POST -H "Content-Type: application/json" -d '{"email": "<email>"}' https://loco.bweston.uk/api/authenticateEmail
        
        HTTP/2 200 
        server: nginx/1.18.0
        date: Thu, 07 Apr 2022 13:45:39 GMT
        content-type: application/json
        content-length: 17
        strict-transport-security: max-age=31536000; includeSubDomains

        {"success":true}
    
    .. note::
        You should replace ``<email>`` with the email you want to authenticate.
    
    This will send an OTP to the email that you provide. You should use this in the next step.
#. Create an account using :http:post:`/api/createUser`:
    
    .. code-block:: bash
            
        $ curl -i -X POST -H "Content-Type: application/json" -d '{"email": "<email>", "OTP": <OTP>, "fullName": "<fullName>", "hostFlag": <true/false>}' https://loco.bweston.uk/api/createUser

        HTTP/2 200 
        server: nginx/1.18.0
        date: Thu, 07 Apr 2022 13:54:48 GMT
        content-type: application/json
        content-length: 157
        strict-transport-security: max-age=31536000; includeSubDomains

        {"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1IiJ9.eyJpYXQiOjE2NDkzMzk2ODgsInN1YiI6ImIud2VzdG9uNjBAZ21haWwuY29tIn0.u7XHubo_5b4QfHWgLu-OCJgUTpI4F_ERS1ePDODBBMQ"}
        
    .. note::
        You should repace all the values in ``<>`` with your information. Make sure to pay attention to quotation marks so your input is valid JSON for each datatype.

You can then call any other API endpoint using this ``token``. Refer below for the JSON attributes that you need to supply, what will be returned and a description of each call.


Submodules
----------

Server.api.authenticateEmail module
-----------------------------------

.. autoflask:: Server:create_app()
   :modules: Server.api.authenticateEmail

Server.api.createEvent module
-----------------------------

.. autoflask:: Server:create_app()
   :modules: Server.api.createEvent

Server.api.createGroup module
-----------------------------

.. autoflask:: Server:create_app()
   :modules: Server.api.createGroup

Server.api.createUser module
----------------------------

.. autoflask:: Server:create_app()
   :modules: Server.api.createUser

Server.api.getAttendance module
-------------------------------

.. autoflask:: Server:create_app()
   :modules: Server.api.getAttendance

Server.api.getEvent module
--------------------------

.. autoflask:: Server:create_app()
   :modules: Server.api.getEvent

Server.api.getUser module
-------------------------

.. autoflask:: Server:create_app()
   :modules: Server.api.getUser

Server.api.getUsersFromGroup module
-----------------------------------

.. autoflask:: Server:create_app()
   :modules: Server.api.getUsersFromGroup

Server.api.setAttendance module
-------------------------------

.. autoflask:: Server:create_app()
   :modules: Server.api.setAttendance

Module contents
---------------

.. autoflask:: Server:create_app()
   :modules: Server.api
   
.. autofunction:: Server.api.update()
