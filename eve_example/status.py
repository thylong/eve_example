from flask import jsonify
from eve.utils import config


def register(app):
    @app.route('/status')
    def status():
        """Return the application status.

        This is the health check endpoint for PaaS services.
        """
        return jsonify({config.STATUS: config.STATUS_OK})
