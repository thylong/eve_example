zips = {
    'schema': {
        'city': {
            'type': 'string',
            'unique': True
        },
        'loc': {
            'type': 'list',
        },
        'state': {
            'type': 'string',
            'regex': '^[A-Z]{2}$',
        },
        'state_id': {
            'type': 'string',
        },
        'pop': {
            'type': 'integer',
        }
    },
    'resource_methods': ['GET'],
    'item_methods': ['GET'],
}

# Version of the endpoint for admins
from copy import deepcopy
zips_schema = deepcopy(zips['schema'])
# Make sure every fields are writable by admins
for key in zips_schema.keys():
    zips_schema[key]['readonly'] = False

admin_zips = {
    'url': '_admin/zips',
    'datasource': {
        'source': 'accounts',
    },
    'schema': zips_schema,
    'allowed_roles': ['super'],
    'allowed_item_roles': ['super'],
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'PUT', 'DELETE'],
}
