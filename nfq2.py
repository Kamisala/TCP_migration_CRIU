# encoding:utf-8
import os
import socket,scapy
import time

from scapy.all import *
from netfilterqueue import NetfilterQueue


#3.20 在nfq 的基础上：修改迁移方式， 不使用arp表，转而使用scapy 修改mac地址
os.system('iptables -A FORWARD -d 10.0.1.1 -j NFQUEUE --queue-num 1')
os.system('iptables -A FORWARD -s 10.0.1.1 -j NFQUEUE --queue-num 1')
os.system('iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP')

# 定义要检测的字符串和替换的字符串
search_str = 'password'
replace_str = 'attack'

# 定义要修改的目的MAC地址和源IP地址
target_mac = '00:00:00:00:00:34'
source_ip = '10.0.1.1'

state=0
def udp_client(ip, port, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(message.encode(), (ip, port))
    client_socket.close()

def udp_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', port))
    while True:
        message, address = server_socket.recvfrom(1024)
        if message.decode() == 'restore_over':
            server_socket.close()
            break

# 定义处理数据包的回调函数
def handle_packet(packet):
    global state
    # 解析数据包 可以直接插入到scapy
    pkt = IP(packet.get_payload())

    # 检测payload中是否包含指定的字符串
    if pkt.haslayer(TCP) and search_str in str(pkt[TCP].payload) and state==0:
#执行dump 并等待restore
        udp_client('10.0.3.3', 5005, 'dump')
        time.sleep(2)
        udp_client('10.0.3.4', 5005, 'restore')
        time.sleep(8)

        # 更新数据包的payload并发送
        # os.system('arp -s 10.0.3.3 00:00:00:00:00:34')
        # state=1
        packet.accept()
        state=1
    elif(state==1 and pkt.src == '10.0.1.1'):
        sendp(Ether(dst='00:00:00:00:00:34', src='00:00:00:00:00:11') / pkt, iface='gateway-eth1')

    else:
        # 将数据包放回队列
        packet.accept()



# 创建NetfilterQueue对象并绑定到指定的队列号
queue_num = 1
nfqueue = NetfilterQueue()
nfqueue.bind(queue_num, handle_packet)

# 打印提示信息
print(f'Starting packet capture on queue {queue_num}...')

# 进入主循环
try:
    nfqueue.run()
except KeyboardInterrupt:
    os.system('iptables -F')
    pass

# 关闭NetfilterQueue对象
nfqueue.unbind()

