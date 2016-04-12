from eve import Eve
from .settings import DEFAULT_SETTINGS
from . import status

modules = {
    status
}

app = Eve(settings=DEFAULT_SETTINGS)

for module in modules:
    module.register(app)

application = app
