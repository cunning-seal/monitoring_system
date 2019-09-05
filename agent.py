#!/usr/bin/env python -W ignore::UserWarning
import psutil, socket
from struct import pack
from time import sleep
import sys
import psycopg2
import signal
import multiprocessing as mp
from time import sleep
import struct

PROXY_UDP_HOST = 'localhost'
PROXY_UDP_PORT = 5107

TCP_HOST = 'localhost'
TCP_PORT = 5108

BYTES_IN_MB = 2097152

abonent_id = 1234

HW_METRIC_TYPE = 1
DB_STATIC_METRIC_TYPE = 111
DB_DYNAMIC_METRIC_TYPE = 112
# адрес сервера-приёмника



class UdpProxyServer:
    def __init__(self):
        # адрес прокси сервера
        self.UDP_HOST = PROXY_UDP_HOST
        self.UDP_PORT = PROXY_UDP_PORT

        # адрес сервера-приёмника
        self.TCP_HOST = TCP_HOST
        self.TCP_PORT = TCP_PORT

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.settimeout(1)
        try:
            server.bind((self.UDP_HOST, self.UDP_PORT))
        except socket.error:
            print("[E][PROXY] Ошибка привязки сокету к адресу")
            raise

        try:
            client = socket.create_connection((self.TCP_HOST, self.TCP_PORT))
        except socket.error:
            print("[E][PROXY] Ошибка соединения с сервером обработки данных")
            raise
        print("[S][PROXY] Соединение с сервером обработки данных установлено")

        def signal_handler(signal, frame):
            print("[E][PROXY] SIGTERM получен")
            server.close()
            sys.exit(0)

        signal.signal(signal.SIGTERM, signal_handler)


        while (True):
            try:
                print("[S][PROXY] Ожидание пакета данных")
                received, reply_address = server.recvfrom(2*BYTES_IN_MB)
                print(received)
                client.send(received)
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                server.close()
                sys.exit()



def static_finder(argv):
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # client = socket.create_connection((TCP_HOST, TCP_PORT))
            break
        except socket.timeout:
            print("[E][STATIC] Таймаут соединения. Проверьте работу прокси сервера и при необходимости перезапустите его")
            continue
    print("[S][STATIC] Соединение с прокси сервером установлено")

    if len(argv) != 0:
        HOST = argv[0]
        USER = argv[1]
        PSWD = argv[2]
        # создание соединения с сервером базы данных
        while True:
            try:
                conn = psycopg2.connect(host=HOST,user=USER, password=PSWD)
                cursor = conn.cursor()
                break
            except:
                print("[E][STATIC] Ошибка создания соединения с базой данных")
                sleep(1)
                continue
        print("[S][STATIC] Соединение с базой данных установлено")


    def signal_handler(signal, frame):
        print("[E][STATIC] SIGSTP получен")
        client.close()
        cursor.close()
        conn.close()
        sys.exit(0)

    signal.signal(signal.SIGTSTP, signal_handler)


    try:
        while True:

            # # hardware part
            try:
            #     # для астры
            #     # temp = psutil.sensors_temperatures()['acpitz']
            #     # for x in temp:
            #     #     TEMPERATURE += int(x.current)
            #     #     if TEMPERATURE >= int(x[0].critical)*0.9:
            #     #         print("GORIM!")
            #
            #     # для убунты
                temp = psutil.sensors_temperatures()['coretemp']
                t = 0
                for x in temp:
                    if int(x.current) > t:
                        t = int(x.current)
                if int(x.current) >= int(x.critical)*0.9:
                    print("[W][STATIC] Перегрев CPU")
                TEMPERATURE = t

                CPU = int(psutil.cpu_percent())
                # sending hardware data
                hw_data = pack('<iii', abonent_id, TEMPERATURE, CPU)
                length = len(hw_data)
                TYPE = pack('>H', HW_METRIC_TYPE)
                LENGTH = pack('<H', length)
                MESSAGE = TYPE + LENGTH + hw_data

                client.sendto(MESSAGE, (PROXY_UDP_HOST, PROXY_UDP_PORT))
                # client.sendto(MESSAGE, (SEND_UDP_HOST, SEND_UDP_PORT))
            except:
                print("[E][STATIC] Ошибка сбора или отправки статистики аппаратного обеспечения")
                e = sys.exc_info()[1]
                print("[E][STATIC] " + str(e.args[0]))

            if len(argv) != 0:
                # database part
                STATUS = True
                CON_NUM = 0
                MAX_CON_NUM = 0
                RBACK_PROCENT = 0
                DB_SIZE = 0
                try:

                    cursor.execute("select count(*) from pg_stat_activity;")
                    CON_NUM = cursor.fetchone()[0]

                    cursor.execute("show max_connections;")
                    MAX_CON_NUM = int(cursor.fetchone()[0])


                    # TODO объединить запросы
                    cursor.execute("select xact_rollback from pg_stat_database;")
                    rb_num = 0
                    for db_tuple in cursor.fetchall():
                        rb_num += db_tuple[0]
                    cursor.execute("select xact_commit from pg_stat_database;")
                    com_num = 0
                    for db_tuple in cursor.fetchall():
                        com_num += db_tuple[0]
                    RBACK_PROCENT = round(rb_num/com_num, 2)

                    cursor.execute("select pg_database_size(pg_database.datname) from pg_database;")
                    DB_SIZE = 0
                    # size in Gb
                    for db_tuple in cursor.fetchall():
                        DB_SIZE+=db_tuple[0]/1073741824
                except:
                    STATUS = False

                try:
                    print(STATUS, CON_NUM, MAX_CON_NUM, RBACK_PROCENT, DB_SIZE)
                    db_data = pack('<i?IIff', abonent_id, STATUS, CON_NUM, MAX_CON_NUM, RBACK_PROCENT, DB_SIZE)
                    length = len(db_data)
                    TYPE = pack('>H', DB_STATIC_METRIC_TYPE)
                    LENGTH = pack('<H', length)
                    MESSAGE = TYPE + LENGTH + db_data
                    client.sendto(MESSAGE, (PROXY_UDP_HOST, PROXY_UDP_PORT))
                except:
                    print("[E][STATIC] Не удалось отправить статистику по серверу баз данных")

            sleep(5)
    except KeyboardInterrupt:
        client.close()
        if len(argv) != 0:
            cursor.close()
            conn.close()
        sys.exit()

# def dynamic_finder(host, port, mb_size):
#
#     server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     server.settimeout(1)
#
#
#     def signal_handler1(signal, frame):
#         print("[E] SIGNAL IS CATCHED")
#         server.close()
#         sys.exit(0)
#
#     def signal_handler2(signal, frame):
#         print("[E] SIGNAL IS CATCHED")
#         server.close()
#         sys.exit(0)
#
#     signal.signal(signal.SIGTERM,signal_handler1)
#     signal.signal(signal.SIGTSTP,signal_handler2)
#
#     try:
#         server.bind((host, port))
#     except socket.error:
#         print("[E] BIND ERROR")
#         sys.exit(1)
#     print("GOTCHA!")
#     while (True):
#         try:
#             # TODO как в сишную структуру завернуть в qt? для тупеньких)))))
#             received, reply_address = server.recvfrom(2 * mb_size)
#             print(received)
#             r = received.split("_")
#             pid, = struct.unpack("<H", r[0])
#
#             print(pid)
#             name = psutil.Process(pid).name()
#             print(name)
#
#
#         except socket.timeout:
#             continue
#         except KeyboardInterrupt:  # TODO отработать SIG_TERM
#             server.close()
#             return

if __name__ == '__main__':
    if sys.argv[1] == "1":
        static_finder(sys.argv[2:])
    elif sys.argv[1] == "2":
        proxy = UdpProxyServer()
        proxy.run()
    elif sys.argv[1] == "3":
        # pass
        proxy = UdpProxyServer()
        p1 = mp.Process(group=None, name="HW_AND_DB_METRIC_FROM_SERVER", target=static_finder, args=(sys.argv[2:],))
        p2 = mp.Process(group=None, name="DB_METRIC_FROM_CLIENTS", target=proxy.run)

        p1.start()
        p2.start()

        pid1 = p1.pid
        pid2 = p2.pid
        print(pid1,pid2)
        print(p1, p1.is_alive())
        print(p2, p2.is_alive())
        while True:
            try:
                pass
            except KeyboardInterrupt:
                p1.terminate()
                p2.terminate()

                print(p1, p1.pid, p1.is_alive())
                print(p2, p2.pid, p2.is_alive())
                sys.exit()
