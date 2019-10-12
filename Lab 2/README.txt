File Name: README
Author: Aisha Iftikhar
Class: CSE 3461 

This lab implements a file-transfer protocol that includes a server called ftps.py and a client caled ftpc.py. 

The server-side file can be run by using the command:
	
	python3 ftps.py <port number>

where <port number> is an available port on the local server.

The client-side file can be run once the server side script has been launched by using the command:

	python3 ftpc.py <remote IP> <remote port number> <local file to transfer>

<remote IP> is the IP address or host name of the remote server (where the server script was run)
<remote port number> is the port number from the server side script 
<local file to transfer> is the name of a file located on the local client server that is to be transferred

When the transfer if complete, the program will run a MF5 checksum comparison to ensure the two files are bitwise identical. The transferred file will be located in the recv directory 
