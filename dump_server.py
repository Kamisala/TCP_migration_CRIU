# encoding:utf-8
import socket,os,time

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((UDP_IP, UDP_PORT))

os.system('./replace.sh file.txt password_1.txt')
print ('file.txt is password_1.txt now')

pid=-1

while True:
    data, addr = server_socket.recvfrom(1024)
    print("Received message: ", data.decode())
    if data.decode().isdigit():
        pid=data.decode()
    if data.decode() == "dump":
        os.system('sudo python3 criu-ns dump -v4 -o criu.log -t '+pid+' -j --tcp-established -D ./criu')

        print ('dump ,over')
        break
