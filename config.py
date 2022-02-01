import os

DEBUG = False
access_authentication = False

# DB_NAME = os.getenv('DB_NAME')
# DB_USER = os.getenv('DB_USER')
# DB_PASS = os.getenv('DB_PASS')
# DB_HOST = localhost
# DB_PORT = 5432


if DEBUG is True:
    from config_local import *