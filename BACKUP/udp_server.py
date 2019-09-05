import sys, os, re, socket, struct, signal
from django.dispatch import Signal, receiver
from django import setup


# путь к проекту. Если находится в другой папке - изменить
sys.path.append('/home/firstsite')
os.environ['DJANGO_SETTINGS_MODULE']='firstsite.settings'
from admin_info.signals import broken_package_signal
BYTES_IN_MB = 2097152
RECV_BUFFER_IN_MB = 5

MAX_BUFFER_SIZE = 100

class ServerApp:
    def __init__(self, s):
        self.UDP_PORT = 7777
        self.UDP_HOST = 'localhost'
        self.SIGNALS = s
        print("SERVER APP CREATED")

    def run(self):

        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.settimeout(1)
        try:
            server.bind((self.UDP_HOST, self.UDP_PORT))
        except socket.error:
            print("BIND ERROR")
            raise

        def signal_handler(signal, frame):
            print("SIGTERM IS CATCHED")
            server.close()
            sys.exit(0)

        signal.signal(signal.SIGTERM, signal_handler)

        setup()

        while (True):
            try:


                loaded = False
                previous_loaded = False

                print("WAITING FOR PACKAGE")
                # заголовочные 4 байта - отдельно
                received, reply_address = server.recvfrom(2*BYTES_IN_MB)
                print(received)

                try:
                    # первые 2 байта - тип метрики, вторые 2 байта - длина пакета
                    type, length = struct.unpack('<HH', received[:4])
                except:
                    desc = "PROBLEMS WITH UNPACKING HEADER"
                    print(desc)
                    broken_package_signal.send(sender=self.__class__, description=desc, data=str(received))
                    continue

                if length >= RECV_BUFFER_IN_MB*BYTES_IN_MB:
                    desc = "TOO LARGE AMOUNT OF DATA. DROPPING PACKAGE"
                    print(desc)
                    broken_package_signal.send(sender=self.__class__, description=desc, data=str(received))
                    continue

                if length != len(received[4:]):
                    desc = "BROKEN PACKAGE"
                    broken_package_signal.send(sender=self.__class__, description=desc, data=str(received))
                    print(desc)
                    continue

                #определяем какие сигналы нужно будем прокинуть
                try:
                    sig_list = self.SIGNALS[str(type)]
                    print("TYPE: ",type)
                    print("SIGNALS: ",sig_list)
                except KeyError:
                    desc = "UNDEFINED SIGNAL TYPE"
                    print(desc)
                    broken_package_signal.send(sender=self.__class__, description=desc, data=str(received))
                    continue

                full_data = received[4:]



                for signal_data in sig_list:
                    s = signal_data['sig_obj']
                    try:
                        s.send(sender=self.__class__, data=full_data)
                    except:
                        desc = "ERROR ON SENDING SIGNALS TO DJANGO SIDE"
                        broken_package_signal.send(sender=self.__class__, description=desc, data=str(received))
                        e = sys.exc_info()[1]
                        print(e.args[0])


            except socket.timeout:
                continue
            except KeyboardInterrupt:
                server.close()
                return

def define_signals():
    from firstsite.settings import INSTALLED_APPS
    metrics_apps = []
    SIGNALS_LIST = []
    #получаем список приложений
    for application in INSTALLED_APPS:
        flag = re.findall(r'django', application)
        if len(flag) == 0 and application != 'receiver_app':
            metrics_apps.append(application)

    # из каждого приложения тянем из signals.py (если есть) SIGNALS - список со словарями
    # вида {sig_type: int, sig_obj: Signal}
    for x_app in metrics_apps:
        dest = x_app + '.signals'
        try:
            res = __import__(dest, globals(), locals(), ['APP_SIGNALS'])
        except ImportError:
            continue
        for sig_info in res.APP_SIGNALS:
            SIGNALS_LIST.append(sig_info)
    return SIGNALS_LIST

def render_signals(s):
    sig_info = {}
    for sig_dict in s:

        t = sig_dict['sig_type']
        signals = []
        for cycle_sig_dict in s:
            if cycle_sig_dict['sig_type'] == t:
                d = {'sig_obj':cycle_sig_dict['sig_obj'], 'priority':cycle_sig_dict['priority']}
                signals.append(d)
        signals.sort(key=lambda x: x['priority'])
        info = {str(t):signals}
        sig_info.update(info)
    return sig_info

def main():

    SIGNALS = define_signals()
    RENDERED_SIGNALS = render_signals(SIGNALS)
    SERVER = ServerApp(RENDERED_SIGNALS)
    SERVER.run()

if __name__ == '__main__':
    main()