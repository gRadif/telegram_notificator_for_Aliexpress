import os


access_authentication = os.getenv("ACCESS", 'False')


try:
    from config_local import *
except ImportError:
    pass