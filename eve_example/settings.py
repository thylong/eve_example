import os

DEFAULT_SETTINGS = {
    'SERVICE_NAME': 'eve_example',
    'SERVICE_ENV': os.getenv('SERVICE_ENV', 'dev'),
    'DOMAIN': {
        'zips': {}
    }
}
