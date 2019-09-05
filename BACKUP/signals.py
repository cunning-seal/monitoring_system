from django.dispatch import Signal, receiver
from django.db import InternalError
from struct import unpack
from external_app_set.models import ExternalApp
from internal_apps_set.models import InternalApp
from connection_metrics.models import AbonentConnectionMetric
from sys import exc_info
from datetime import datetime

APP_SIGNALS = []
abonent_connection_info = Signal(providing_args=['data'])
signal_1 = {"sig_type": 2, "sig_obj":abonent_connection_info, 'priority':1}
APP_SIGNALS.append(signal_1)

@receiver(abonent_connection_info)
def abonent_connection_info_callback(sender, **kwargs):
    data = kwargs.get('data')

    app_id, = unpack('<H', data[:2])
    # целое число TAbConState
    app = InternalApp.objects.filter(id=app_id)

    data = data[2:]

    if len(data)%21 != 0:
        print("SMTH WENT WRONG")
    else:
        for i in range(1,len(data)//21+1):
            TAbConState = data[:21*i+1]
            id, connection_number, receivedBytes, sentBytes, timeCon = unpack('<IBIIQ', TAbConState)
            timeCon=datetime.fromtimestamp(timeCon)
            ab = ExternalApp.objects.filter(id=id)

            # .strftime('%Y-%m-%d-%H-%M-%S')


            if len(ab) != 0 and len(app)!=0:
                metric = AbonentConnectionMetric(abonent=ab[0],connections_number=connection_number, receivedBytes=receivedBytes, sentBytes=sentBytes, app=app[0], timeCon=timeCon)
            elif len(ab)==0:
                x = ExternalApp(id=id,name='UndefinedAbonent')
                x.save()
                metric = AbonentConnectionMetric(abonent=x, connections_number=connection_number, receivedBytes=receivedBytes, sentBytes=sentBytes, app=app[0], timeCon=timeCon)
            else:
                print('THERE IS NO SUCH APPLICATION IN LIST')
                raise InternalError
            try:
                metric.save()
            except:
                e = exc_info()[1]
                print(e.args[0])