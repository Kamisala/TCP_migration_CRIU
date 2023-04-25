# CRIU-enabled-Migration
This project uses CRIU and netfilterqueue to conduct a server migration experiment: when transferring files (file.txt) between the client and the server, netfilterqueue is used to detect whether the payload content contains "password" characters. If so, send a "dump" signal to the running dump_server to let dump_server record the current state. At the same time, the gateway (Gateway) will send a "restore" signal to restore_server on another host, asking restore_server to modify the file content and restore the previous state. restore_server will start a new server process to restore the previously dumped server and transfer the modified file to the client.
## Design Topology
![image](https://user-images.githubusercontent.com/105418310/234154876-b6563286-3c9f-4b8b-be8d-0413e126a670.png)
In the non-migration case, when the Client starts the client.py program, it will download the file.txt file from the server.py on DumpHost, which has the same content as password_1.txt. We assume that this is the real password file, and we do not want its content to be stolen. Therefore, we use NetfilterQueue (nfq.py) on the Gateway to detect the content of the packets. If certain keywords, such as "password," are detected, we will migrate FlowS1 to FlowS2 and send the "dump" command to DumpHost (actually dump_server.py) and the "restore" command to RestoreHost (actually restore_server.py). At this point, DumpHost stops sending the file.txt file and stores the server process as an image file. Then, RestoreHost replaces the content of the file.txt file with password_2.txt, creates an IP address that the server process binds to, and uses CRIU to restore the server process, which will continue to send the content of file.txt to the client. Finally, the receive.txt file received by the Client will contain the first half of the content of password_1.txt and the second half of the content of password_2.txt. 
## Experiment Procedure

Launch mn.py on the terminal of the virtual machine, and then open terminals for gateway, reHost, and dumpHost.
Start nfq.py on the gateway. (Steps 2 and 3 can be done in any order.)
Start dump_server.py on the dumpHost. Replace file.txt with password_1.txt.
Start server.py on the dumpHost after launching dump_server.py. Send the server's PID to dump_server.
Start client.py on the client.
A. Connect to the server, and download the file.txt from the server.
B. During the transmission, when the nfq module detects that the payload contains the sensitive keyword "password":
a. Discard the packet.
b. Send a "dump" signal to the dump_server.
- dump_server saves the state of the server.
c. Send a "restore" signal to the restore_server.
- restore_server assigns an additional IP address to the local host reHost (using the address bound by server.py).
- restore_server replaces the content of file.txt with password_2.txt.
- restore_server restores the server process on the local host reHost.
d. Modify the local ARP table to redirect network traffic from client and dumpHost to client and reHost.
The client continues to receive file.txt from reHost until the end of the transmission. At this point, the client has received file.txt with the first portion constructed from password_1.txt, and the remaining portion with the content of password_2.txt.
（Specific content can view the video）
## Contributing
This experiment provides a feasible idea to preserve state in network layer, transport layer, and application layer migration in applicable scenarios
## Contact

LLY - atomy.lly@gmail.com
