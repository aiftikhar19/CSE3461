# File Name: ftps.py
# Author: Aisha Iftikhar
# Class: CSE 3461 

import socket
import sys
import os.path
import hashlib

CHUNK_SIZE = 1000
HOST = socket.gethostname()	# host IP address
PORT = int(sys.argv[1])		# arbitrary non-privileged port
TROLLPORT = int(sys.argv[2])

# make subdir 
subDir = "recv/"
if not os.path.exists(subDir):
	os.makedirs(subDir)

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print ("Socket Created")
print ("The host is : %s"%HOST)

# Bind socket, print error if failed
s.bind((HOST,PORT))

# let user know socket is listening
print ("Socket listening...")

duplicate_data = b""
bytesRead = 0

while 1:
	data, addr = s.recvfrom(1000)		# receive 1000 bytes
	clientIP_encoded = data[0:4]		# first 4 bytes = IP address
	clientPORT_encoded = data[4:6]		# next 2 bytes = PORT
	ACK_encoded = data[7:8]

	# ACK duplicate
	if duplicate_data == data:
		s.sendto(clientIP_encoded+clientPORT_encoded+ACK_encoded, ("",TROLLPORT)) # send ACK
		print ("Duplicate Packet")
	else:
		duplicate_data = data
		s.sendto(clientIP_encoded+clientPORT_encoded+ACK_encoded, ("",TROLLPORT)) # send ACK

		# check flag = 1 for size 
		if (int.from_bytes(data[6:7], byteorder="big") == 1):
			byte_size = data[8:len(data)]
			size = int.from_bytes(byte_size,byteorder="big")# convert size from bytes -> int
			print ("Size of file: ", size)

		# check flag = 2 for filename
		if (int.from_bytes(data[6:7], byteorder="big") == 2):
			byte_filename = data[8:len(data)]		# decode filename
			filename = byte_filename.decode()

			if filename.rfind("/"):				# support for files not in same directory
				index = filename.rfind("/")
			filename = filename[index+1:]
			filename = filename.lstrip() 			# byte to string & strip zero
			print ("Name of file: ", filename)

			# open file to be writing
			writeFile = open(subDir + filename, "wb")

		# check flag = 3 for actual data
		if (int.from_bytes(data[6:7], byteorder="big") == 3):
			data = data[8:len(data)]
			writeFile.write(data)				# read data and write to file stream
		
			# stops execution of loop at EOF
			if len(data) < 960:
				break

# close file streams
writeFile.close()
s.close()
print ("Transfer Complete. Socket Closed.")

# check to make sure the new file is bitwise identical to the original 
newFile = open(subDir + filename, "rb")
oldFile = open(filename, "rb")

# use md5 checksum hashing algorithm 
oldHash = hashlib.md5()
newHash = hashlib.md5()

print("Checking files...")

while True:
    oldData = oldFile.read(CHUNK_SIZE)
    newData = newFile.read(CHUNK_SIZE)
    if oldData:
        oldHash.update(oldData)
        newHash.update(newData)
    else:
        break

print("The two files are bitwise identical: " + str(oldHash.hexdigest() == newHash.hexdigest()))

# close file streams
oldFile.close()
newFile.close()
