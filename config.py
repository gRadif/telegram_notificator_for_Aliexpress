import os


access_authentication = True

if DEBUG is True:
    try:
        from config_local import *
    except ImportError:
        pass