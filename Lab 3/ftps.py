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

subDir = "recv/"
if not os.path.exists(subDir):
	os.makedirs(subDir)
		
# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print ("Socket Created.")

# bind socket
s.bind((HOST,PORT))
print ("Socket listening...")

# read data
while 1:
	data, addr = s.recvfrom(CHUNK_SIZE)	# receive 1000 bytes
	clientIP_encoded = data[0:4]		# IP addres in the first 4 bytes
	clientPORT_encoded = data[4:6]		# Port number in next 2 bytes

	if (int.from_bytes(data[6:7], byteorder="big") == 1):	# check flag for size
		byte_size = data[7:len(data)]			# after byte 7 the actual data is transmitted
		size = int.from_bytes(byte_size, byteorder="big")	# convert size from bytes to int

		print ("Size of file: ", size)

	if (int.from_bytes(data[6:7], byteorder="big") == 2):	# check flag for filename
		byte_filename = data[7:len(data)]
		filename = byte_filename.decode()		# decode filename
		
		if filename.rfind("/"):				# support for files not in same directory
			index = filename.rfind("/")
		filename = filename[index+1:]
		filename = filename.lstrip()			# convert byte to string & strip zero

		print ("Name of file: ", filename)

		# open file write
		writeFile = open(subDir + filename, "wb")

	if (int.from_bytes(data[6:7], byteorder="big") == 3):	# check flag for data
		data = data[7:len(data)]
		writeFile.write(data)				# read data and write to file stream
		if data == b"":					# stops execution of loop at EOF
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
