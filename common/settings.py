# -*- coding: utf-8 -*-
# HINT: str.encode("UTF-8")
MONGO_SERVER = '127.0.0.1'
MONGO_PORT = 27017
MEMCACHED_SERVER = '127.0.0.1'
MEMCACHED_PORT = 11211
SPHNX_IP = '127.0.0.1'
SPHNX_PORT = 3312
SPHNX_LIMIT = 500

SPHNX_LIMIT_REPORT = 3000
MONGO_LIMIT_REPORT = 10000

DEBUG = False  # True = crash on exceptions

try:
    from common.local_settings import *
except ImportError:
    pass
