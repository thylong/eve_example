import os
from .zips.domain import zips

DEFAULT_SETTINGS = {
    'SERVICE_NAME': 'eve_example',
    'SERVICE_ENV': os.getenv('SERVICE_ENV', 'dev'),

    'MONGO_URI': os.getenv('MONGO_URI', 'mongodb://mongo:27017/eve_example'),

    'DOMAIN': {
        'zips': zips
    }
}
