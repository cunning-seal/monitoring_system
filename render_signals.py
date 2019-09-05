import re
import sys, os, re, socket, struct, signal
from django.dispatch import Signal, receiver
import django
sys.path.append('/home/firstsite')
os.environ['DJANGO_SETTINGS_MODULE']='firstsite.settings'

def define_signals():
    from firstsite.settings import INSTALLED_APPS
    metrics_apps = []
    SIGNALS_LIST = []
    # получаем список приложений
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