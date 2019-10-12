CSE 3461 Lab 4
Aisha Iftikhar

To run, open four terminal windows. In two, connect to a CSE remote server; this will be system 2. In the other two, connect to a second CSE server; these will be system 1. The file server.txt within this directory lists the client and server IP addresses and ports I used to run this program.

On system 2, run the command:
% python3 ftps.py <local-port-on-System-2> <troll-port-on-System-2>

On system 1, run the command:
% troll -C <IP-address-of-System-1> -S <IP-address-of-System-2> -a <client-port-on-System-1> -b <server-port-on-System-2> <troll-port-on-System-1> -t -x <packet-drop-\%>
	
	***NOTE: client port on system 1 is hardcoded to be 3200

On system 2, run the command:
% troll -C <IP-address-of-System-2> -S <IP-address-of-System-1> -a <server-port-on-System-2> -b <client-port-on-System-1> <troll-port-on-System-2> -t -x <packet-drop-\%>

On system 1, run the command:
% python3 ftpc.py <IP-address-of-System-2> <remote-port-on-System-2> <troll-port-on-System-1> \<local-file-to-transfer>

In this program, it is assumed that all input is done correctly. In addition, depending on the percentage of packets dropped, the program may take up to 1 minute to execute. Once the file is transferred, the program performs an MD5 checksum to determine if the files are bitwise identical. If true, the system will output:
	The two files are bitwise identical: True
If false, the system will output:
	The two files are bitwise identical: False
