import logging
import os

from flask import Blueprint

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."
__version__ = "0.0.1"
__description__ = "WebHawk Flask Web Initiator"
__abs_dirpath__ = os.path.dirname(os.path.abspath(__file__))

# Create the Flask App
website_blueprint = Blueprint('website', __name__, template_folder='templates',
                              static_folder='static', static_url_path='web/static')

# Start the views
from . import views


def bootstrap(flask_app, config):
    """
    Bootstrap the Bluprint

    :param flask_app: The Flask object
    :param config: Application Config
    """

    # Get logger
    logger = logging.getLogger("webhawk")
    logger.info("WebHawk Website Initiated")
