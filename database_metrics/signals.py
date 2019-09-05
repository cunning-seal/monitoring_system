from django.dispatch import Signal, receiver
from struct import unpack
from sys import exc_info
from datetime import datetime
from .models import ServerDBMetric
from abonents.models import Abonent
import sys

SIGNAL_TYPE = 111

APP_SIGNALS = []
db_info = Signal(providing_args=['data'])
signal_1 = {"sig_type": SIGNAL_TYPE, "sig_obj":db_info, 'priority':1}
APP_SIGNALS.append(signal_1)

@receiver(db_info)
def db_info(sender, **kwargs):
    data = kwargs.get('data')

    abonent_id, status, con_num, max_con_num,rback_perc,db_size = unpack('<i?IIff', data)
    ab = Abonent.objects.filter(computer_id=abonent_id)
    if(len(ab) != 0):
        metric = ServerDBMetric(db_abonent=ab[0], db_work_status=status,max_connections_number=max_con_num,connections_number=con_num,rollback_percent=rback_perc,database_size=db_size)
    else:
        ab = Abonent.objects.filter(computer_id=0000)
        metric = ServerDBMetric(db_abonent=ab[0], db_work_status=status,max_connections_number=max_con_num,connections_number=con_num,rollback_percent=rback_perc,database_size=db_size)
    try:
        metric.save()
        print("[S] Метрика сохранена, номер типа ", SIGNAL_TYPE)
    except:
        print("[E] Ошибка при сохранении метрики, номер типа ", SIGNAL_TYPE)
        e = sys.exc_info()[1]
        print(print(e.args[0]))
