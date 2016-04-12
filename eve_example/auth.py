import os
from eve.auth import BasicAuth


class SimpleBasicAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        return username == 'admin' and password == os.environ.get('ADMIN_PASSWORD', '')  # pragma: no cover
