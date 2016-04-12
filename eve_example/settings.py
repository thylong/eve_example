import os

DEFAULT_SETTINGS = {
    'SERVICE_NAME': 'revshare',
    'SERVICE_ENV': os.getenv('SERVICE_ENV', 'dev'),
    'DOMAIN': {
        'zips': {}
    }
}
