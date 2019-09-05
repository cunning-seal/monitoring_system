import sys, os, re, socket, struct, signal
from django.dispatch import Signal, receiver
import django

from render_signals import render_signals,define_signals

BYTES_IN_MB = 2097152
RECEIVE_BUFFER_IN_MB = 5

MAX_BUFFER_SIZE = 100

class UdpProxyServer:
    def __init__(self):
        # адрес прокси сервера
        self.UDP_HOST = 'localhost'
        self.UDP_PORT = 5107

        # адрес сервера-приёмника
        self.TCP_HOST = 'localhost'
        self.TCP_PORT = 5108

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.settimeout(1)
        try:
            server.bind((self.UDP_HOST, self.UDP_PORT))
        except socket.error:
            print("[E] BIND ERROR")
            raise

        try:
            client = socket.create_connection((self.TCP_HOST, self.TCP_PORT))
        except socket.error:
            print("[E] TCP CONNECT ERROR")
            raise
        print("[S] Client connection succesfull")

        def signal_handler(signal, frame):
            print("[E] SIGTERM IS CATCHED")
            server.close()
            sys.exit(0)

        signal.signal(signal.SIGTERM, signal_handler)


        while (True):
            try:
                print("[S] WAITING FOR PACKAGE")
                received, reply_address = server.recvfrom(2*BYTES_IN_MB)
                print(received)
                client.send(received)
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                server.close()
                return


def main():

    server = UdpProxyServer()
    server.run()

if __name__ == '__main__':
    main()
