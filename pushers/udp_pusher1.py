# udp_pusher to hardware_metrics

import socket, struct
from random import randint
from time import sleep

UDP_IP = 'localhost'
UDP_PORT = 5107

# тип метрики
type = 1
# данные для передачи
data = struct.pack('<iii', 1234, 10, 20)
# длина пакета
length = len(data)

abonents_ID = [1234,5678,9012]

MESSAGE = struct.pack('<hh', type, length) + data

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        choosed_id = randint(0,2)
        id = abonents_ID[choosed_id]
        temperature = randint(35,70)
        cpu_load = randint(0,100)
        data = struct.pack('<iii', id, temperature, cpu_load)
        # длина пакета
        length = len(data)

        MESSAGE = struct.pack('<hh', type, length) + data

        print(MESSAGE)
        client.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        sleep(5)
except KeyboardInterrupt:
    client.close()
