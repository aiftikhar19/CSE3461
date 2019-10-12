# File Name: ftpc.py
# Author: Aisha Iftikhar
# Class: CSE 3461

import time 
import socket
import sys  
import os.path
import select

CHUNK_SIZE = 960
HOST = sys.argv[1]    		     # client server host
PORT = int(sys.argv[2])              # client server port
TROLLPORT = int(sys.argv[3])	     # troll port
filename = sys.argv[4]  	     # file to transfer

HOSTIP = socket.gethostbyname(socket.getfqdn(HOST))	# input HOST, get IP
HOSTIP_encoded = socket.inet_aton(HOSTIP)		# IP converted to bytes
PORT_encoded = PORT.to_bytes(2, byteorder="big")	# port converted to bytes

# create UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
print ("Socket Created") 

# bind socket
s.bind((socket.gethostname(),3200))
print ("Socket bound to port 3200")

# gets size of file and filename
size = os.path.getsize(filename)
filename = filename.rjust(20)

# set flag
flag = 1
flag_encoded = flag.to_bytes(1, byteorder = "big")	# convert flag to bytes

byte_size = size.to_bytes(4, byteorder = "big")		# convert size to bytes
byte_filename = filename.encode()			# encode filename to bytes

# set ACKs
ACK_NUM = -1
ACK = 0
ACK_encoded = ACK.to_bytes(1, byteorder = "big")	# convert ack to bytes

while ACK != ACK_NUM:
	# send size of file in bytes
	s.sendto(HOSTIP_encoded + PORT_encoded + flag_encoded + ACK_encoded + byte_size, ("", TROLLPORT))
	
	# receive data from socket
	read, write, error = select.select([s], [], [], .05)

	if len(read) > 0:
		ACK_read = read[0].recv(1000)
		ACK_encoded = ACK_read[7:8]
		ACK_NUM = int.from_bytes(ACK_encoded, byteorder = "big")
	# timeout if no ACK
	if [read,write,error] == [ [], [], [] ]:
		print("Timeout...")

print ("File size sent.")
	
flag = 2
flag_encoded = flag.to_bytes(1, byteorder = "big")

# increment ACK
ACK = ACK + 1
ACK_encoded = ACK.to_bytes(1, byteorder = "big")

while ACK!= ACK_NUM:
	# send name of file in bytes
	s.sendto(HOSTIP_encoded + PORT_encoded + flag_encoded + ACK_encoded + byte_filename, ("",TROLLPORT))

	# receive data from socket 
	read, write, error = select.select([s], [], [], .05)

	if len(read) > 0:
		ACK_read = read[0].recv(1000)
		ACK_encoded = ACK_read[6:]
		ACK_NUM = int.from_bytes(ACK_encoded, byteorder = "big")
	# timeout if no ACK
	if [read,write,error] == [ [], [], [] ]:
		print("Timeout...")

print ("File name sent.")

# open file to read
readFile = open(filename.lstrip(), "rb")

flag = 3
flag_encoded = flag.to_bytes(1, byteorder = "big")

data = readFile.read(CHUNK_SIZE)
while data != b"":  
	ACK = ACK + 1
	ACK = ACK % 2
	ACK_encoded = ACK.to_bytes(1, byteorder = "big")

	while ACK != ACK_NUM:		
		# send data in bytes
		s.sendto(HOSTIP_encoded + PORT_encoded + flag_encoded + ACK_encoded + data, ("",TROLLPORT)) 
		
		# receive data from socket
		read, write, error = select.select([s], [], [], .05)

		if len(read) > 0:
			ACK_read = read[0].recv(1000)
			ACK_encoded = ACK_read[6:]
			ACK_NUM = int.from_bytes(ACK_encoded, byteorder = "big")
			time.sleep(.01)
		if [read,write,error] == [ [], [], [] ]:
			print("Timeout...")
	data = readFile.read(960)

s.sendto(HOSTIP_encoded + PORT_encoded + flag_encoded + ACK_encoded + data, ("",TROLLPORT))

# close file streams
readFile.close()
s.close()

print ("Transfer Complete. Socket Closed.")
