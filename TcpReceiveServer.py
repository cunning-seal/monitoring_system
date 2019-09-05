import sys, os, re, socket, struct, signal, _thread
from django.dispatch import Signal, receiver
import django

# путь к проекту. Если находится в другой папке - изменить
sys.path.append('/home/firstsite')
os.environ['DJANGO_SETTINGS_MODULE']='firstsite.settings'
from admin_info.signals import broken_package_signal
BYTES_IN_MB = 2097152
RECEIVE_BUFFER_IN_MB = 5
MAX_CON_NUMBER = 150
from render_signals import render_signals, define_signals


def on_new_client(clientsocket, addr, signals):
    while True:
        try:
            loaded = False
            previous_loaded = False

            print("[S] WAITING FOR PACKAGE")
            # заголовочные 4 байта - отдельно
            received, reply_address = clientsocket.recvfrom(2 * BYTES_IN_MB)
            print(received)

            try:
                # первые 2 байта - тип метрики, вторые 2 байта - длина пакета
                type, = struct.unpack('>H', received[:2])
                length, = struct.unpack('<H', received[2:4])
            except:
                desc = "PROBLEMS WITH UNPACKING HEADER"
                print(desc)
                broken_package_signal.send(sender=TcpReceiveServer.__class__, description=desc, data=str(received))
                continue

            if length >= RECEIVE_BUFFER_IN_MB * BYTES_IN_MB:
                desc = "TOO LARGE AMOUNT OF DATA. DROPPING PACKAGE"
                print(desc)
                broken_package_signal.send(sender=TcpReceiveServer.__class__, description=desc, data=str(received))
                continue

            if length != len(received[4:]):
                desc = "BROKEN PACKAGE"
                broken_package_signal.send(sender=TcpReceiveServer.__class__, description=desc, data=str(received))
                print(desc)
                continue

            # определяем какие сигналы нужно будем прокинуть
            try:
                sig_list = signals[str(type)]
                print("[S] TYPE: ", type)
                print("[S] SIGNALS: ", sig_list)
            except KeyError:
                print("TYPE: ", type)
                desc = "UNDEFINED SIGNAL TYPE"
                print(desc)
                broken_package_signal.send(sender=TcpReceiveServer.__class__, description=desc, data=str(received))
                continue

            full_data = received[4:]

            for signal_data in sig_list:
                s = signal_data['sig_obj']
                try:
                    s.send(sender=TcpReceiveServer.__class__, data=full_data)
                except:
                    desc = "ERROR ON SENDING SIGNALS TO DJANGO SIDE"
                    broken_package_signal.send(sender=TcpReceiveServer.__class__, description=desc, data=str(received))
                    e = sys.exc_info()[1]
                    print("[E] " + str(e.args[0]))


        except socket.timeout:
            continue
        except KeyboardInterrupt:  # TODO отработать SIG_TERM
            clientsocket.close()
            return
        # Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.

    clientsocket.close()

class TcpReceiveServer:
    def __init__(self, s):
        self.PORT = 5108
        self.HOST = 'localhost'
        self.SIGNALS = s
        print("[S] SERVER APP CREATED")

    def run(self):
        print(self.SIGNALS.keys())
        django.setup()
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.bind((self.HOST, self.PORT))
        except socket.error:
            print("[E] BIND ERROR")
            raise


        def signal_handler(signal, frame):
            print("[E] SIGTERM IS CATCHED")
            server.close()
            sys.exit(0)

        signal.signal(signal.SIGTERM, signal_handler)
        server.listen(150)
        while True:
            conn, addr = server.accept()
            print('Got connection from', addr)
            _thread.start_new_thread(on_new_client, (conn, addr, self.SIGNALS))

        server.close()



sys.path.append('/home/firstsite')
os.environ['DJANGO_SETTINGS_MODULE']='firstsite.settings'

if __name__ == '__main__':
    signals = define_signals()
    rendered_signals = render_signals(signals)
    server = TcpReceiveServer(rendered_signals)
    server.run()