# CRIU-enabled-Migration
This project uses CRIU and netfilterqueue to conduct a server migration experiment: when transferring files (file.txt) between the client and the server, netfilterqueue is used to detect whether the payload content contains "password" characters. If so, send a "dump" signal to the running dump_server to let dump_server record the current state. At the same time, the gateway (Gateway) will send a "restore" signal to restore_server on another host, asking restore_server to modify the file content and restore the previous state. restore_server will start a new server process to restore the previously dumped server and transfer the modified file to the client.
## Design Topology
![image](https://user-images.githubusercontent.com/105418310/234154876-b6563286-3c9f-4b8b-be8d-0413e126a670.png)
In the non-migration case, when the Client starts the client.py program, it will download the file.txt file from the server.py on DumpHost, which has the same content as password_1.txt. We assume that this is the real password file, and we do not want its content to be stolen. Therefore, we use NetfilterQueue (nfq.py) on the Gateway to detect the content of the packets. If certain keywords, such as "password," are detected, we will migrate FlowS1 to FlowS2 and send the "dump" command to DumpHost (actually dump_server.py) and the "restore" command to RestoreHost (actually restore_server.py). At this point, DumpHost stops sending the file.txt file and stores the server process as an image file. Then, RestoreHost replaces the content of the file.txt file with password_2.txt, creates an IP address that the server process binds to, and uses CRIU to restore the server process, which will continue to send the content of file.txt to the client. Finally, the receive.txt file received by the Client will contain the first half of the content of password_1.txt and the second half of the content of password_2.txt. 
## Setup

1. Start the `mn.py` script on the virtual machine terminal.
2. Open terminals for the Gateway, restoreHost, and dumpHost.
3. On the Gateway, start the `nfq.py` script.
4. On the restoreHost, start the `restore_server.py` script.
5. On the dumpHost, start the `dump_server.py` script and replace the `file.txt` content with `password_1.txt`.
6. On the dumpHost, start the `server.py` script after starting the `dump_server.py` script and send the server's PID to the dump_server.
7. On the client, start the `client.py` script.

## Experiment Flow

1. The client connects to the server and begins downloading the `file.txt` text file.
2. At some point during the transfer, netfilterqueue detects the string "password" in the payload:
   a. The data packet is discarded.
   
   b. A "dump" signal is sent to the dump_server, which saves the state of the dump server.
   
   c. A "restore" signal is sent to the restore_server, which assigns an additional IP to the local host and modifies the `file.txt` content to `password_2.txt`.
   
   d. The restore_server restores the server process on the local host.
   
   e. The local ARP table is modified to redirect network traffic from client and dumpHost to client and restoreHost.
   
   f. The client continues to receive the `file.txt`, which now contains the content of both `password_1.txt` and `password_2.txt`.
（Specific content can view the video）
## Contributing
This experiment provides a feasible idea to preserve state in network layer, transport layer, and application layer migration in applicable scenarios
## Contact

LLY - atomy.lly@gmail.com
