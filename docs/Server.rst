.. _Server:

Server
==============
This section documents the :ref:`Server` python package.

All documentation relating to the API itself is in the :ref:`Server.api`. This includes exact details of all the endpoints and how to make requests using the command line tool curl_.

.. _curl: https://curl.se/

Module contents
---------------

.. automodule:: Server
   :members:
   :undoc-members:
   :show-inheritance:

Submodules
----------

Server.auth module
------------------

.. automodule:: Server.auth
   :members:
   :undoc-members:
   :show-inheritance:

Server.database module
----------------------

.. automodule:: Server.database
   :members:
   :undoc-members:
   :show-inheritance:

Server.web module
-----------------

.. autoflask:: Server:create_app()
   :blueprints: web
   :undoc-static:

Subpackages
-----------

.. toctree::
   :maxdepth: 4

   Server.api
