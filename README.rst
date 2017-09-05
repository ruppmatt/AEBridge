===========================
Avida-ED Diagnostic Utility
===========================
Author: Matthew Rupp
Institution: Michigan State University
Date: 2016-10-10


Introduction
============

`Avida-ED Web <https://avida-ed.beacon-center.org>`_ is the education version of the digital life research platform Avida.  This software package enables a user to monitor the communication between the webpage user interface and the Avida web worker by using `SocketIO <http://http://socket.io/>`_ duplex communication.  


Usage
=====

This package requires Python 3.  The required Python packages are stored in the requirements.txt and may
be installed using pip.  It is strongly recommended that a Python virtual environment is used with this
project.


Setting up a Python virtual environment
---------------------------------------


Install redis
-------------


Starting the server
-------------------
To start the server:
  + Start redis on port 5060
  + Load the python virtual environment
  + Run ws_server.py



Features
========

ws_server.py
------------

``ws_server.py`` contains the Flask and flask_socketio code that enables full duplex support between the Avida web worker and additional clients such as the messages page described below and provies a `redis <http://redis.io/>`_ database which stores compressed, seralized JSON messages between the avida web worker and its clients.  Because redis allows for atomic operations, additional redis-aware processes (e.g. another instance of python) can make use of the data stored by ``ws_server``.



messages.html
-------------

A special webpage named ``messages.html`` displays the JSON messages sent between the hosts and the clients.

The following types of messages are relayed to a special messages webpage:

1. Messages sent from the user interface webpage
#. Messages sent from the avida web worker to the user interface
#. Debug messages generated internally from the Avida byte-code (if so compiled)
#. Messages sent from an external source (e.g. a python session).

Messages are color coded and marked with symbols to determine where they originate.  Currently:

Blue
   Message originates from the user interface

Green
   Message originates as a response from the Avida web worker

Gray
   Message is internal to the messsages webpage

Orange
   Message originates as a compiled-in debug statement

Red
   Message echos an external (non-UI) command from another client (e.g. a python console)


Message headers display information about each message.  The type of message followed by a colon and then a message name is used to help easily interpret the contents of each message.  A left-facing cheveron before the message heading means the message was sent *to* the Avida web worker; a right-facing cheveron means the message was sent *from* the Avida web worker.

The number(s) next to each message heading are to be read as [ db_ndx @ transmission_update ].  The ``db_ndx`` refers to the numerical key in the redis database that holds the entire message.  (Note: Use the ``GetMessage`` method from ``ws_server`` to retrieve the message.  The displayed index is not the full document key; and the message is also stored in a compressed format.)

Messages may be loaded by clicking on their individual heading; and unloaded the same way.  Because some messages can be quite large, messages are removed from the DOM when their JSON information is no longer available.

Because all messages are in JSON format, a modified version of a `port of JSONView <https://github.com/yesmeck/jquery-jsonview>`_ is used to help navigate the material send between the Avida worker and the client(s).

Something changed...

cmd_socket.py
-------------
``cmd_socket.py`` provides a few lines of code to make use of `socketio-client <https://pypi.python.org/pypi/socketIO-client>_ in order to send messages through ``ws_server`` to the Avida web worker.  Simply click on an element to expand the JSON object.
