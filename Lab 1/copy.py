# CSE 3461 Lab 1
# File name: copy.py
# Created by: Aisha Iftikhar
# Creation date: 1/11/19
# Synopsis: Write a program called copy.py in Python that reads a file and creates a copy of it in a sub-directory named recv (on the same system)

import sys
import os
import hashlib

# create recv directory if it does not exist
if not os.path.exists("recv"):
    os.makedirs("recv")

# read in file name and open
filename = str(sys.argv[1])
file = open(filename, "rb")   #'r' used to open file for reading, and 'b' opens it in binary

# open a file in the recv directory for writing
copyFile = open("recv/" + filename, "wb") #'w' opens file for writing, creates the file if doesn't exist

# loop through file, continue to read the data in 1000 byte blocks and then writing to new file
while True:
    data = file.read(1000)
    if data:
        copyFile.write(data)
    else:
        break

# close file streams
file.close()
copyFile.close()

# print result
print("File <" + filename + "> has been successfully copied to the recv directory.")

# check to make sure the new file is bitwise identical to the original 
newFile = open("recv/" + filename, "rb")
oldFile = open(filename, "rb")

# use md5 checksum hashing algorithm 
oldHash = hashlib.md5()
newHash = hashlib.md5()

print("Checking files...")

while True:
    oldData = oldFile.read(1000)
    newData = newFile.read(1000)
    if data:
        oldHash.update(oldData)
        newHash.update(newData)
    else:
        break

print("The two files are bitwise identical: " + str(oldHash.hexdigest() == newHash.hexdigest()))

#close file streams
oldFile.close()
newFile.close()
