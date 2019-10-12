# File Name: ftps.py
# Author: Aisha Iftikhar
# Class: CSE 3461 

import socket
import sys
import os
import hashlib

# Declare global variables
CHUNK_SIZE = 1000
FILE_SIZE = 4
FILE_NAME_SIZE = 20

HOST = ""		# Symbolic name meaning all available interfaces
PORT = int(sys.argv[1])	# Arbitrary non-privileged port

# the new file created by ftps.py should be in a different direcotry to  
# avoid overwriting original files
# create recv directory if it doesn't already exist
subDir = "recv/"
if not os.path.exists(subDir):
	os.makedirs(subDir)

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind socket
s.bind((HOST, PORT))

# allow one connection
s.listen(1) 
print ("Socket listening...")

# print address
conn, addr = s.accept()
print ("Connected by ", addr)

# the first 4 bytes will contain the number of bytes to follow
data = conn.recv(FILE_SIZE)
size = int.from_bytes(data, byteorder="big")
print("File Size: ", size)

# the next 20 bytes will contain the name of the file
data = conn.recv(FILE_NAME_SIZE)
filename = data.decode("utf-8")

# support for files not in the same directory
if filename.rfind("/"):
	index = filename.rfind("/")

# format file name string
filename = filename[index+1:]
filename = filename.lstrip()
print("File Name: ", filename)

# open file to write
writeFile = open(subDir + filename, "wb")

bytesRead = 0
while bytesRead < size: 
	data = conn.recv(CHUNK_SIZE)
	bytesRead += len(data)
	writeFile.write(data)

# close file streams
writeFile.close()	
conn.close()		

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
