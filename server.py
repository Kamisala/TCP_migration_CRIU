# encoding:utf-8
# encoding:utf-8
# encoding:utf-8
# encoding:utf-8
import socket, os
import time




pid = os.getpid()
print("Process ID is:", pid)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(bytes(str(pid), "utf-8"), ('10.0.3.3', 5005))

HOST = '10.0.3.3'  # 服务器IP地址
PORT = 8001  # 服务器端口号

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print('等待客户端连接...')
    conn, addr = s.accept()
    print('客户端已连接:', addr)
    with conn:
        start_time = time.time()
        filename = 'file.txt'  # 文件名
        with open(filename, 'rb') as f:
            l = f.read(1024)  # 每次读取1024字节

            while (l):
                conn.send(l)
                print('sending '+l.decode())
                l = f.read(1024)
                time.sleep(1)
        print('文件传输完成')

        end_time = time.time()
        total_time = end_time - start_time
        time.sleep(10)

        # print(f"Total time: {total_time} seconds")
