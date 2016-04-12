import os
import random

MONGO_DBNAME = os.getenv('MONGO_DBNAME', 'test_eve_example_%s' % random.randint(1000, 9999))
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongo:27017/%s' % MONGO_DBNAME)
DEBUG = True
