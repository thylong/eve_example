from eve import Eve
from .settings import DEFAULT_SETTINGS
from .auth import SimpleBasicAuth
from . import status

modules = {
    status
}

app = Eve(settings=DEFAULT_SETTINGS, auth=SimpleBasicAuth)

for module in modules:
    module.register(app)

application = app
