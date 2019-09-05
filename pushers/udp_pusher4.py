# undefined signal type

import socket, struct
from time import sleep



UDP_IP = 'localhost'
UDP_PORT = 7777

# тип метрики
type = 4
data = b'some_dangerous_data'
# длина пакета
length = len(data)

MESSAGE = struct.pack('<hh',type,length) + data

addr = (UDP_IP, UDP_PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    while True:
        client.sendto(MESSAGE, addr)
        sleep(30)
except KeyboardInterrupt:
    client.close()
