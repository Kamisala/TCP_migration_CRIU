# encoding:utf-8
import socket,os,time

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((UDP_IP, UDP_PORT))

# os.system('./0_my2.sh 0_file.txt password_1.txt')
# print ('0_file.txt is password_1.txt now')

while True:
    data, addr = server_socket.recvfrom(1024)
    print("Received message: ", data.decode())
    if data.decode() == "restore":
        os.system('ifconfig reHost-eth1 10.0.3.3')
        os.system('./replace.sh file.txt password_2.txt')
        #filename = '0_file.txt'  # 文件名
        #with open(filename, 'rb') as f:
         #   print (f.read(200).decode())

        time.sleep(3)

        os.system('sudo python3 criu-ns restore -v4 -o criu.log -j --tcp-established -D ./criu')
        print ('restore ,over')
        break

