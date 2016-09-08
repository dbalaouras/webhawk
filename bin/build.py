#!/usr/bin/env python
import logging.config
import os
import sys

__abs_dirpath__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append("%s/../webhawk/" % __abs_dirpath__)

from lib.common import print_logo
from optparse import OptionParser
from repositories.recipe_repository import FileRecipeRepository
from services.app_context import AppContext
from services.builder import Builder
from services.config_loader import ConfigLoader
from services.git_manager import GitManager
from services.multiprocess_task_queue import MultiprocessTaskQueue

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."
__version__ = "0.0.1"
__status__ = "Prototype"
__description__ = "WebHook Command Line Builder"


def build(cli_options, repository, branch):
    """
    Starts the build

    :param cli_options: Command line options
    :param repository: Repository name
    :param branch: Branch name
    """

    config = ConfigLoader(cli_options=cli_options)

    # TODO: Validate config

    # Setup logging
    logging.config.dictConfig(config['logging'])
    logger = logging.getLogger("webhawk")

    logger.info("=== Running WebHawk CLI ===")

    context = AppContext(allow_replace=False)
    context.register("config", config)
    context.register("logger", logger)
    context.register("task_queue", MultiprocessTaskQueue(context=context))
    context.register("recipe_repository", FileRecipeRepository(context=context))
    context.register("git_manager", GitManager(context=context))
    context.register("builder", Builder(context=context))

    recipe = context["recipe_repository"].find_by_name_and_branch(name=repository, branch=branch)

    if not recipe:
        logger.error("Could not find Recipe for %s:%s" % (repository, branch))
        exit(1)

    # Create a new build id if one does not exist
    context["builder"].run(build_id=Builder.generate_build_id(), repository_name=repository, branch_name=branch)


def parse_options():
    """
    Parses all options passed via the command line
    """

    # Define version and usage strings
    usage = "python %prog [options]"

    # Initiate the cli options parser
    parser = OptionParser(usage=usage, version=__version__, description=__description__)

    # Define available command line options

    parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False,
                      help="Debug")

    parser.add_option("-r", "--recipes_file_path", action="store", dest="recipes_file_path",
                      default="%s/../config/recipes.yaml" % __abs_dirpath__,
                      help="Path to a yaml file containing the recipes")

    parser.add_option("-w", "--workspace_path", action="store", dest="workspace_path",
                      default="webhawk-builds", help="Branch to build")

    parser.add_option("-t", "--builder_hostname", action="store", dest="builder_hostname",
                      default="localhost",
                      help="Hostname of the build machine (for remote builds; uses ~/.ssh/config config")

    parser.add_option("-a", "--repository", action="store", dest="repository",
                      default=None, help="Repository to build")

    parser.add_option("-b", "--branch", action="store", dest="branch",
                      default=None, help="Branch to build")

    parser.add_option("-c", "--cleanup_builds", action="store_true", dest="cleanup_builds",
                      default=False, help="Cleanup build directory after build")

    # Parse the options
    (options, args) = parser.parse_args()

    if not options.repository or not options.branch:  # if filename is not given
        parser.print_help()
        parser.error('A repository AND branch must be both specified')
        sys.exit(1)

    return options, args


if __name__ == '__main__':
    """
    Entry point of this module. This method will be invoked first when running the app.
    """

    # Parse command line options
    (cli_options, cli_args) = parse_options()

    print_logo()

    build(cli_options=cli_options, repository=cli_options.repository, branch=cli_options.branch)
