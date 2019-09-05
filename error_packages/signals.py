from django.dispatch import Signal,receiver
import struct
from error_packages.models import Error_Metric
from abonents.models import Abonent
from internal_apps_set.models import InternalApp

SIGNAL_TYPE = 3

APP_SIGNALS = []
error_signal = Signal(providing_args=['data'])
signal_1 = {'sig_type':SIGNAL_TYPE, 'sig_obj':error_signal, 'priority':1}
APP_SIGNALS.append(signal_1)

@receiver(error_signal)
def error_callback(sender,**kwargs):
    data = kwargs.get('data')

    computer_id, importance_level = struct.unpack('<ib',data[:5])
    info_string = data[5:]
    res = info_string.split(b'\t')
    code_type = res[0].decode('latin-1')
    programm = res[1].decode(code_type)
    subprocess = res[2].decode(code_type)
    description = res[3].decode(code_type)
    ab = Abonent.objects.filter(computer_id=computer_id)[0]
    app = InternalApp.objects.filter(name=programm)[0]


    if app.abonent.computer_id !=computer_id:
        print("NO SUCH APPLICATION ON THIS COMPUTER")
        # скинуть в базу с ошибками
        return
    metric = Error_Metric(abonent=ab, importance_level=importance_level,app=app,subprocess=subprocess,description=description)
    try:
        metric.save()
        print("[S] Метрика сохранена, номер типа ", SIGNAL_TYPE)
    except:
        print("[E] Ошибка при сохранении метрики, номер типа ", SIGNAL_TYPE)
