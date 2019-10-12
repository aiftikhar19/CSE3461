# File Name: ftpc.py
# Author: Aisha Iftikhar
# Class: CSE 3461

import time 
import socket
import sys  
import os.path

CHUNK_SIZE = 960
HOST = socket.gethostname()
IP_ADDR = sys.argv[1]		# client server host
PORT = int(sys.argv[2])		# client server port
TROLLPORT = int(sys.argv[3])	# troll port
filename = sys.argv[4]		# file to transfer

HOSTIP = socket.gethostbyname(socket.getfqdn(IP_ADDR))	# input HOST, grab the IP
HOSTIP_encoded = socket.inet_aton(HOSTIP)		# IP converted to bytes
PORT_encoded = PORT.to_bytes(2, byteorder="big")	# Port converted to bytes

# create UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
print ("Socket Created") 

# attempt to bind the hardcoded socket
s.bind((HOST,3456))
print ("Socket binded to 3456")

# gets the size of file and the filename
size = os.path.getsize(filename)
filename = filename.rjust(20)

# set flags
flag = 1
flag_encoded = flag.to_bytes(1, byteorder = "big")	# convert flag to bytes

byte_size = size.to_bytes(4, byteorder = "big")		# convert size to bytes
byte_filename = filename.encode()			# encode filename to bytes

# send size and filename in bytes
s.sendto(HOSTIP_encoded + PORT_encoded + flag_encoded + byte_size, ("", TROLLPORT))
print ("File size sent.")

flag = 2
flag_encoded = flag.to_bytes(1, byteorder = "big") 	# flag to bytes

s.sendto(HOSTIP_encoded + PORT_encoded + flag_encoded + byte_filename, ("",TROLLPORT))
print ("File name sent.")

# open file to read 
readFile = open(filename.lstrip(), "rb")

flag = 3
flag_encoded = flag.to_bytes(1, byteorder = "big")	# flag to bytes

# read bytes until EoF
data = readFile.read(CHUNK_SIZE)
while data != b"":  
	s.sendto(HOSTIP_encoded + PORT_encoded + flag_encoded + data, ("",TROLLPORT))
	time.sleep(.01)					# sleep to prevent overloading of buffer
	data = readFile.read(CHUNK_SIZE)

s.sendto(HOSTIP_encoded+PORT_encoded+flag_encoded+data, ("",TROLLPORT))

# close file streams
readFile.close()
s.close()

print ("Transfer Complete. Socket Closed.")

