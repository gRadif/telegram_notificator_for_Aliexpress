import os

DEBUG = True
access_authentication = False

DB_NAME = os.getenv
DB_USER = os.getenv
DB_PASS = os.getenv
DB_HOST = '127.0.0.1'
DB_PORT = 5432

token = os.getenv('TOKEN')


if DEBUG is True:
    try:
        from config_local import *
    except ImportError:
        pass