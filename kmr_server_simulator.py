#!/usr/bin/env python

# to allow for socket communication
import socket
import sys
import time

print(sys.version)

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 30002  # Arbitrary non-privileged port

# open a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

# bind socket to host and port, also catch exception.
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print('Socket bind complete')

# start listening to the socket
s.listen(10)
print('Socket now listening')

conn, addr = s.accept()
print ('Connected with ' + addr[0] + ':' + str(addr[1]))

while 1:
    client_request = conn.recv(1024)
    print('client request is: %s' % client_request)
    msg = input('Enter a message for haas: ')
    try:
        conn.sendall(msg)
        if not msg is "b'(3)/n'":
            print "start message is: b'(3)/n' "
    except:
        print "send string or binary format pe. b'(3)/n'"
        pass
    time.sleep(0.1)

conn.close()
s.close()
