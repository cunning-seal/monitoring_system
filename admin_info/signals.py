from django.dispatch import Signal, receiver
from admin_info.models import BrokenPackage


APP_SIGNALS = []
broken_package_signal = Signal(providing_args=['data','d_type', 'description'])

@receiver(broken_package_signal)
def broken_package_reciever(sender, **kwargs):
    data = kwargs.get('data')
    description = kwargs.get('description')
    bp = BrokenPackage(data=data, description=description, code=0)
    try:
        bp.save()
    except:
        print("ERROR IN SAVING PROCESS")