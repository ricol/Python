#!/usr/bin/env python
#-*- coding: utf-8 -*-

import socket
    # Import socket module

s = socket.socket()  # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 12345  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port

s.listen(5)  # Now wait for client connection.
print("Server is running...")
while True:
    c, addr = s.accept()  # Establish connection with client.
    print('Got connection from', addr)
    c.send('Thank you for connecting')
    c.close()  # Close the connection
print("Server quit.")
