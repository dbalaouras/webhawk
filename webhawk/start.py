#!/usr/bin/env python
import logging
import os
from optparse import OptionParser

from flask import Flask

from lib.common import print_logo
from services.config_loader import ConfigLoader

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."
__version__ = "0.0.1"
__description__ = "WebHawk Flask Application Launcher"
__abs_dirpath__ = os.path.dirname(os.path.abspath(__file__))

# Declare Flask up here
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True


def bootstrap(flask_webapp, cli_options=None):
    """
    Bootstraps the Web App
    :return:
    """
    global app

    # TODO: Validate config
    config = ConfigLoader(cli_options=cli_options)
    logging.config.dictConfig(config['logging'])

    logger = logging.getLogger("webhawk")
    logger.info("=== WebHawk Services Starting ===")

    # Import and bootstrap the rest blueprint
    import rest
    rest.bootstrap(flask_app=app, config=config)

    # Import and bootstrap the rest blueprint
    import web
    web.bootstrap(flask_app=app, config=config)

    # Register blueprints
    flask_webapp.register_blueprint(rest.api_blueprint, url_prefix='/api')
    flask_webapp.register_blueprint(web.website_blueprint, url_prefix='/')

    return flask_webapp


def parse_options():
    """
    Parses all options passed via the command line.
    """

    # Define version and usage strings
    usage = "python %prog [options]"

    # Initiate the cli options parser
    parser = OptionParser(usage=usage, version=__version__, description=__description__)

    # Define available command line options

    parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False,
                      help="Debug")

    parser.add_option("-c", "--config", action="store", dest="config_file", default=None,
                      help="Path to a yaml configuration file")

    parser.add_option("-H", "--host", action="store", dest="host", default="0.0.0.0",
                      help="Web server host")

    parser.add_option("-P", "--port", type="int", action="store", dest="port", default=5000,
                      help="Web server port")

    # Parse the options
    (options, args) = parser.parse_args()

    return options, args


if __name__ == '__main__':
    """
    Entry point of this module. This method will be invoked first when running the app.
    """
    print_logo()

    # Parse command line options
    (cli_options, cli_args) = parse_options()

    # Create the app
    bootstrap(flask_webapp=app, cli_options=cli_options)

    # Start the app
    app.run(
        debug=cli_options.debug,
        host=cli_options.host,
        port=cli_options.port
    )
else:
    # Running via wsgi
    bootstrap(flask_webapp=app)
