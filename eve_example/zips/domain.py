zips = {
    'query_objectid_as_string': True,
    'schema': {
        'city': {
            'type': 'string',
        },
        'loc': {
            'type': 'integer',
        },
        'state': {
            'type': 'string',
            'regex': '^[A-Z]{2}$',
        },
        'state_id': {
            'type': 'string',
        },
        'pop': {
            'type': 'string',
        }
    },
    'resource_methods': ['GET'],
    'item_methods': ['GET'],
}
