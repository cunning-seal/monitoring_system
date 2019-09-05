# udp_pusher to connection_metrics
import struct, socket
from random import randint
from time import sleep
from datetime import datetime

UDP_HOST = 'localhost'
UDP_PORT = 5108

# тип метрики
TYPE = 0x6705
#TODO данные для передачи (изменить)

int_app = [123,567,7596]
ext_app = [987,765,432]


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)





try:
    while True:
        # app = int_app[randint(0, 2)]
        app = int_app[0]
        DATA = struct.pack('<H', app)
        num = randint(0,2)

        for i in range(num):
            ab = ext_app[num]
            # conNum = randint(0, 20)
            conNum = 0
            if(conNum == 0):
                recvB = 0
                sentB = 0
            else:
                recvB = randint(0,2**10-1)
                sentB = randint(0,2**10-1)

            timeCon = int((datetime.now()).timestamp())
            DATA += struct.pack('<IBIIQ', ab, conNum,recvB,sentB,timeCon)
        LENGTH = len(DATA)
        print(DATA)
        h1 = struct.pack('>H', TYPE)
        h2 = struct.pack('<H', LENGTH)

        msg = h1 + h2 + DATA
        client.sendto(msg, (UDP_HOST, UDP_PORT))
        sleep(10)

except KeyboardInterrupt:
    client.close()
