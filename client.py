# encoding:utf-8
import socket
import os
import time
start_time = time.time()
pid = os.getpid()
print("Process ID is:", pid)
HOST = '10.0.3.3' # 服务器IP地址
PORT = 8001 # 服务器端口号
flag=0# criu暂停时 给一定时间缓冲

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('connect to server successfully')
    with open('received.txt', 'wb') as f:
        while True:
            try:
                data = s.recv(1024) # 每次接收1024字节
                f.write(data)
                if not data:
                    print('Connection closed by remote host')
                    break
            except Exception as e:
                break
    print('over receive')



# Your code here

end_time = time.time()
total_time = end_time - start_time

print(f"Total time: {total_time} seconds")
