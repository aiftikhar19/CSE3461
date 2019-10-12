CSE 3461 Lab 1
Aisha Iftikhar

To run copy.py:
1. Navigate to the directory in which the script is located, 
2. Type in the command:
	python3 copy.py <filename>
   where <filename> is replaced by the name of the file you wish to copy. 
   NOTE: The file you wish to copy must also be located within the same directory  as the script.
3. Run the script
4. The copy of the file will be located within the recv subdirectory. 

How the script executes:
1. The script will first create a new recv directory if one is not present.
2. The file will be copies into the recv directory 1000 bytes at a time. Once complete, a message will print, saying the file has been copied successfully. 
3. The copied file is now validated by checking the hashed md5 checksum. If the files are identical, the script will print that the files are bitwise identical. Otherwise, it will print false. 
