# udp_pusher to hardware_metrics

import socket, struct
from random import randint
from time import sleep

UDP_IP = 'localhost'
UDP_PORT = 7777

# тип метрики
type = 1
# данные для передачи
data = struct.pack('<iii', 1234, 10, 20)
# длина пакета
length = len(data)

msg = struct.pack('<hh', type, length) + data

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


client.sendto(msg, (UDP_IP, UDP_PORT))

client.close()
