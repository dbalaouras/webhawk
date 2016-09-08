#!/usr/bin/env python

import logging.config
import os
from optparse import OptionParser

from flask import Flask
from flask import redirect
from flask import send_from_directory
from flask_restful import Api

from lib.common import print_logo
from repositories.recipe_repository import FileRecipeRepository
from rest.api_errors import ApiErrorRegistry
from rest.bitbucket_webhook import BitBucketWebHook
from rest.recipe import Recipe
from rest.root import Root
from services.app_context import AppContext
from services.build_task_manager import BuildTaskManager
from services.builder import Builder
from services.config_loader import ConfigLoader
from services.git_manager import GitManager
from services.multiprocess_task_queue import MultiprocessTaskQueue

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."
__version__ = "0.0.1"
__description__ = "WebHawk Flask Application Launcher"
__abs_dirpath__ = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)


def bootstrap_app(flask_web_app, cli_options=None):
    """
    Create a Flask app

    :param flask_web_app: The Flask App to Bootstrap
    :param cli_options: Command line options (for direct execution of this script vs wsgi)
    :return: The Flask Application to bootstrap
    """

    config = ConfigLoader(cli_options=cli_options)

    # TODO: Validate config

    # Create the Flask app and the API
    flask_web_app.config['PROPAGATE_EXCEPTIONS'] = True

    # Setup logging
    logging.config.dictConfig(config['logging'])
    logger = logging.getLogger("webhawk")

    logger.info("=== WebHawk Services Starting ===")

    # Create the context
    # TODO: put the following names in a single class as static strings
    context = AppContext(allow_replace=False)
    context.register("config", config)
    context.register("logger", logger)
    context.register("task_queue", MultiprocessTaskQueue(context=context))
    context.register("recipe_repository", FileRecipeRepository(context=context))
    context.register("git_manager", GitManager(context=context))
    context.register("builder", Builder(context=context))

    # Start Worker Greenlets
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        task_manager = BuildTaskManager(context=context)
        task_manager.start_workers()
        context.register("task_manager", task_manager)

    # Register error handlers
    ApiErrorRegistry.register_error_handlers(flask_web_app)

    # Create the flask_restful api
    api = Api(flask_web_app)

    # Add Resources to API
    Recipe.add_resource_to_api(api, context=context)
    Root.add_resource_to_api(api, context=context)
    BitBucketWebHook.add_resource_to_api(api, context=context)

    # Redirect to the API path
    if config["base_path"] != '/':
        @flask_web_app.route('/')
        def index():
            return redirect(config["base_path"])

    @flask_web_app.route('/favicon.ico')
    @flask_web_app.route('/favico.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'favicon.ico', mimetype='image/vnd.microsoft.icon')

    logger.info("WebHawk RESTful API Initiated")

    return flask_web_app


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

    parser.add_option("-P", "--port", action="store", dest="port", default=5000,
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
    bootstrap_app(flask_web_app=app, cli_options=cli_options)

    # Start the app
    app.run(
        debug=cli_options.debug,
        host=cli_options.host,
        port=cli_options.port
    )
else:
    # Running via wsgi
    bootstrap_app(flask_web_app=app)
