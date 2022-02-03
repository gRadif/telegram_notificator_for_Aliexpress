import os


access_authentication = os.getenv("ACCESS", 'False')
token = os.getenv("token", '')

try:
    from config_local import *
except ImportError:
    pass