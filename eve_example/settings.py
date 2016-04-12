import os
from .zips.domain import zips, admin_zips

DEFAULT_SETTINGS = {
    'SERVICE_NAME': 'eve_example',
    'SERVICE_ENV': os.getenv('SERVICE_ENV', 'dev'),
    'ADMIN_PASSWORD': os.getenv('ADMIN_PASSWORD', ''),

    'MONGO_URI': os.getenv('MONGO_URI', 'mongodb://mongo:27017/eve_example'),

    'DOMAIN': {
        'zips': zips,
        'admin_zips': admin_zips
    }
}
