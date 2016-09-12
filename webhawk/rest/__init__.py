import logging.config
import os

from flask import Blueprint
from flask_restful import Api

from repositories.recipe_repository import FileRecipeRepository
from rest.api_errors import ApiErrorRegistry
from rest.bitbucket_webhook import BitBucketWebHook
from rest.github_webhook import GithubWebHook
from rest.gitlab_webhook import GitlabWebHook
from rest.recipe import Recipe
from rest.root import Root
from services.app_context import AppContext
from services.build_task_manager import BuildTaskManager
from services.builder import Builder
from services.git_manager import GitManager
from services.multiprocess_task_queue import MultiprocessTaskQueue

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."
__version__ = "0.0.1"
__description__ = "WebHawk Flask Web Initiator"

# Create the Flask App
api_blueprint = Blueprint('api', __name__, url_prefix='/api')


def bootstrap(flask_app, config):
    """
    Bootstra

    :param flask_app: The Flask object
    :param config: Application Config
    """
    global api_blueprint
    # Create the Flask App

    # Get logger
    logger = logging.getLogger("webhawk")

    # Create the context
    # TODO: put the following key names in a single class as static strings
    context = AppContext(allow_replace=False)
    context.register("config", config)
    context.register("logger", logger)
    context.register("task_queue", MultiprocessTaskQueue(context=context))
    context.register("recipe_repository", FileRecipeRepository(context=context))
    context.register("git_manager", GitManager(context=context))
    context.register("builder", Builder(context=context))

    # Start Worker Greenlets
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        task_manager = BuildTaskManager(context=context)
        task_manager.start_workers()
        context.register("task_manager", task_manager)

    # Register error handlers
    ApiErrorRegistry.register_error_handlers(api_blueprint)

    # Create the flask_restful api
    rest_api = Api(api_blueprint)

    # Add Resources to API
    Recipe.add_resource_to_api(rest_api, context=context)
    Root.add_resource_to_api(rest_api, context=context)
    BitBucketWebHook.add_resource_to_api(rest_api, context=context)
    GithubWebHook.add_resource_to_api(rest_api, context=context)
    GitlabWebHook.add_resource_to_api(rest_api, context=context)

    logger.info("WebHawk RESTful API Initiated")
