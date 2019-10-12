CSE 3461 Lab 3
Aisha Iftikhar

To run, open three terminal windows. In one, connect to a CSE remote server; this will be system 2. In the other two, connect to a second CSE server; these will be system 1. The file server.txt within this directory lists the client and server IP addresses and ports I used to run this program.

On system 2, run the command:
	python3 ftps.py <port-on-System-2>

On one system 1 window, run the command:
	troll -C <IP-address-of-System-1> -S <IP-address-of-System-2> -a 3456 -b <port-on-System-2> -r -s 1 -t -x 0 <troll-port-on-System-1>

	***NOTE: Client port is hardcoded as 3456***

On the second system 1 window, run the command:
	python3 ftpc.py <IP-address-of-System-1> <port-on-System-2> <troll-port-on-System-1> <local-file-to-transfer>

In this program, it is assumed that all input is done correctly. Once the file is transferred, the program performs an MD5 checksum to determine if the files are bitwise identical. If true, the system will output:
	The two files are bitwise identical: True
If false, the system will output:
	The two files are bitwise identical: False
