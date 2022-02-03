import os


access_authentication = os.getenv("ACCESS", 'False')

if DEBUG is True:
    try:
        from config_local import *
    except ImportError:
        pass