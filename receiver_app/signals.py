from django.dispatch import Signal, receiver


type_error_from_server = Signal(providing_args=['sig_type', 'addr', 'length'])



@receiver(type_error_from_server)
def type_error_from_server(sender, **kwargs):
    sig_type = kwargs.get('sig_type')
    addr = kwargs.get('addr')
    length = kwargs.get('length')

    print({'sig_type':sig_type, 'addr':addr, 'length':length})
    return