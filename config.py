import os


access_authentication = os.getenv("ACCESS", 'False')
token = os.getenv("token", '')
id_dev = os.getenv('id_dev', '')

try:
    from config_local import *
except ImportError:
    pass
