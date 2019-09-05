from django.dispatch import Signal, receiver
from struct import unpack
from external_app_set.models import ExternalApp
from internal_apps_set.models import InternalApp
from .models import AbonentConnectionMetric
from sys import exc_info
from datetime import datetime

SIGNAL_TYPE = 0x6705

APP_SIGNALS = []
abonent_connection_info = Signal(providing_args=['data'])
signal_1 = {"sig_type": SIGNAL_TYPE, "sig_obj":abonent_connection_info, 'priority':1}
APP_SIGNALS.append(signal_1)

@receiver(abonent_connection_info)
def abonent_connection_info_callback(sender, **kwargs):
    data = kwargs.get('data')

    app_id, = unpack('<H', data[:2])
    app = InternalApp.objects.filter(id=app_id)
    if len(app) == 0:
        raise InternalApp.DoesNotExist("[E] INTERNAL APP DOESN'T EXIST")
    data = data[2:]
    if len(data)%21 != 0:
        raise Exception("[E] DATA SIZE IS NOT MULTIPLIED 21")
    else:
        for i in range(0,len(data)//21):
            TAbConState = data[21*i:21*(i+1)]
            id,connection_number, receivedBytes, sentBytes, timeCon = unpack('<IBIIQ', TAbConState)
            print(str(app_id)+" "+str(id)+" "+str(connection_number)+" "+str(receivedBytes)+" "+str(sentBytes)+" "+str(timeCon))
            timeCon=datetime.fromtimestamp(timeCon)
            ab = ExternalApp.objects.filter(id=id)

            # .strftime('%Y-%m-%d-%H-%M-%S')


            if len(ab) != 0:
                metric = AbonentConnectionMetric(abonent=ab[0],connections_number=connection_number, receivedBytes=receivedBytes, sentBytes=sentBytes, app=app[0], timeCon=timeCon)
            else:
                x = ExternalApp(id=id, name='UndefinedAbonent_' + str(id))
                try:
                    x.save()
                except:
                    raise Exception("[E] ERROR ON CREATING EXTERNAL APP OBJECT")
                metric = AbonentConnectionMetric(abonent=x, connections_number=connection_number, receivedBytes=receivedBytes, sentBytes=sentBytes, app=app[0], timeCon=timeCon)
            try:
                metric.save()
                print("[S] Метрика сохранена, номер типа ", SIGNAL_TYPE)
            except:
                print("[E] Ошибка при сохранении метрики, номер типа ", SIGNAL_TYPE)
