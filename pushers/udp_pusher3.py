# udp_pusher to error_packages
import socket, struct
from random import randint
from time import sleep

UDP_IP = 'localhost'
UDP_PORT = 7777


# тип метрики
TYPE = 3
abonents_id=[1234,5678,9012]

programms = ['App_1', 'App_2', 'App_3','App_4']


addr = (UDP_IP, UDP_PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        computer_id = abonents_id[randint(0, 2)]
        importance_level = randint(1, 7)
        code_type = 'utf-8'

        programm_counter = randint(0,2)

        programm = programms[programm_counter].encode(code_type)
        subprocess = 'PID:234'.encode(code_type)
        description = 'Another error'.encode(code_type)
        code_type = code_type.encode('latin-1')
        f_data = struct.pack('<ib', computer_id, importance_level)
        data = f_data + code_type + b'\t' + programm + b'\t' + subprocess + b'\t' + description
        # длина пакета
        length = len(data)


        # длина пакета
        length = len(data)

        MESSAGE = struct.pack('>H', TYPE) + struct.pack('<H', length) + data

        client.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        sleep(5)
except KeyboardInterrupt:
    client.close()