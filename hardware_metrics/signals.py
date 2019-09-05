from django.dispatch import receiver, Signal
from hardware_metrics.models import Total_Hardware_Metric
from abonents.models import Abonent
from struct import unpack
import sys

# слушает данные по hw_metric, в data лежит bytes с информацией. Парсит, создаёт запись в таблице
# kwargs = словарь с 'data'
# первые 2 байта - длина, в big endian

SIGNAL_TYPE = 1

APP_SIGNALS = []
hw_total_metric_info = Signal(providing_args=['data'])
signal_1 = {"sig_type": SIGNAL_TYPE, "sig_obj":hw_total_metric_info, "priority":1}
APP_SIGNALS.append(signal_1)



@receiver(hw_total_metric_info)
def hw_metric_callback(sender, **kwargs):
    data = kwargs.get('data')

    computer_id, temperature, total_CPU_load = unpack('<iii', data)

    ab = Abonent.objects.filter(computer_id=computer_id)

    if len(ab) != 0:
        metric = Total_Hardware_Metric(abonent=ab[0],temperature=temperature, total_CPU_load=total_CPU_load)
        try:
            metric.save()
            print("[S] Метрика сохранена, номер типа ", SIGNAL_TYPE)
        except:
            print("[E] Ошибка при сохранении метрики, номер типа ", SIGNAL_TYPE)
    else:
        print('There is no such abonent in list!')