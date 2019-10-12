# File Name: ftpc.py
# Author: Aisha Iftikhar
# Class: CSE 3461

import socket
import sys 
import os

# Declare global variables
CHUNK_SIZE = 1000
FILE_SIZE = 4
FILE_NAME_SIZE = 20

IP_ADDR = sys.argv[1]		# the remote host
PORT = int(sys.argv[2])		# the same port as used by the server
filename = str(sys.argv[3])	# filename to transfer

# Create TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Connect to host
s.connect((IP_ADDR, PORT))  
print ("Socket connected to " + IP_ADDR + " on port " + str(PORT)) 

# Check if file exists
if not os.path.exists(filename):
	print("Error: File does not exist. Enter valid filename.")
	print("Exiting program...")
	sys.exit();

# Get file size
size = os.path.getsize(filename)

# format filename
filename = filename.rjust(FILE_NAME_SIZE)

# send size of file in bytes
byte_size = size.to_bytes(FILE_SIZE, byteorder = "big")	
byte_filename = filename.encode()
s.send(byte_size) 
print ("File size sent.")

# send name of file in bytes encoded
s.send(byte_filename) 
print ("File name sent.")

# Open file to read
readFile = open(filename.lstrip(), "rb")

# begin reading data
data = readFile.read(CHUNK_SIZE)
while data != b"":  
	s.send(data)
	data = readFile.read(CHUNK_SIZE)

# close file streams
readFile.close()
s.close()

print ("Transfer Complete. Socket Closed.")
