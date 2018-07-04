import os
import random
import string

from fabric.api import settings, cd, run, local, lcd
from fabric.state import env

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."


class Builder(object):
    """
    Clones and builds remote projects
    """

    def __init__(self, context):
        """
        Class initialization/constructor

        :param context: Application Context
        """

        # Fabric configuration
        env.warn_only = False
        env.use_ssh_config = True

        # Initialize properties
        self._context = context
        self._logger = context.get("logger")
        self._builder_hostname = context["config"]["builder_hostname"]
        self._workspace_path = context["config"]["workspace_path"]
        self._logger.info("Initializing Builder")

        # Use local fabric commands when the builder is localhost
        self._change_dir = lcd if self._builder_hostname == "localhost" else cd

    def run(self, build_id, recipe_id, dependency_build=False):
        """
        Runs the build

        :param build_id: A unique build Id
        :param recipe_id: The id of the Recipe (if known)
        :param dependency_build: Is this a dependency build or not?
        """

        # Check if we have a recipe for the given repository
        recipe = self._context["recipe_repository"].find_one(id=recipe_id)
        # Check if we have dependencies and process them

        # # TODO: check for circular dependencies
        app_dependencies = recipe.get("dependencies", None)
        if app_dependencies:
            for dependency in app_dependencies:
                self.run(build_id=build_id, recipe_id=dependency['recipe_id'], dependency_build=True)

        # Create build path
        build_base_path = self._get_build_base_path(build_id=build_id)
        build_path = "%s/%s" % (build_base_path, recipe_id if recipe_id else recipe["repository"]["name"])

        with settings(host_string=self._builder_hostname, abort_exception=FabricException), self._change_dir(
                self._workspace_path):
            try:
                self._prepare(build_path=build_path)
                if recipe.get('repository', None):
                    self._checkout(recipe=recipe, build_path=build_path)
                self._build(recipe=recipe, build_path=build_path, recipe_id=recipe_id)

            except FabricException as e:
                self._logger.error(
                    "Error occurred while building recipe # %s (build id : %s): %s" % (recipe_id, build_id, e))

            # Cleanup build directory if instructed
            if not dependency_build and self._context["config"]["cleanup_builds"]:
                self._cleanup(build_base_path=build_base_path)

    def _get_build_base_path(self, build_id):
        """
        Constructs a build path
        :return: The build path
        """
        if self._workspace_path[0] != "/":
            # We have a relative path; lets make it absolute for clarity
            current_path = os.getcwd() if self._builder_hostname == "localhost" else self._run_fabric('pwd')
            base_build_path = "%s/%s/%s" % (current_path, self._workspace_path, build_id)
        else:
            base_build_path = "%s/%s" % (self._workspace_path, build_id)

        return base_build_path

    def _prepare(self, build_path):
        """
        Prepare the build directory
        """
        self._logger.info("Preparing Environment %s" % build_path)

        # Make sure the workspace directory exists; otherwise create it
        self._run_fabric('mkdir -p {0}'.format(build_path))

    def _checkout(self, recipe, build_path):
        """
        Checkout the repository
        """
        cms_manager = self._context.get("%s_manager" % recipe["repository"]["vcs"], None)
        cms_manager.clone(url=recipe["repository"]["url"], branch=recipe["repository"]["branch"],
                          target_path=build_path, run_cmd=self._run_fabric)

    def _build(self, recipe, build_path, recipe_id=None):
        """
        Build the repository
        """
        if recipe_id:
            self._logger.info(
                "Building recipe with id %s on %s with command: '%s'" % (recipe_id, build_path, recipe["command"]))
        else:
            self._logger.info("Building %s:%s on %s with command: '%s'" % (
                recipe["repository"]["name"], recipe["repository"]["branch"], build_path, recipe["command"]))

        if recipe.get("command", None):
            with self._change_dir(build_path):
                self._run_fabric("%s" % (recipe["command"]))

        self._logger.info("Finished building")

    def _cleanup(self, build_base_path):
        """
        Cleanup after the build
        """
        self._logger.info("Removing build directory '%s'" % build_base_path)
        self._run_fabric('rm -rf %s' % build_base_path)

    def _run_fabric(self, cmd, log_output=True):
        """
        A Simple wrapper that runs fabric commands and returns the result. This is needed because the builder uses
        either the local or the run command depending on when we're building (localhost vs remote host) and those two
        commands have different stdout capture methods.

        :param cmd: The command to run
        :return: The command stdout
        """
        result = local(cmd, capture=True) if self._builder_hostname == "localhost" else run(cmd)

        if log_output:
            stdout = str(result.stdout)
            stderr = str(result.stderr)

            # Log output
            if stdout:
                self._logger.info("Build stdout: %s" % stdout)

            if stderr:
                self._logger.info("Build stderr: %s" % stderr)

        return result

    @classmethod
    def generate_build_id(cls):
        """
        Generates random build Ids
        :return: The generated build id
        """
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))


class FabricException(Exception):
    """
    An Exception to use as an "abort_exception" of Fabric. Allows better error handling and build failure reporting.
    """

    def __init__(self, *args, **kwargs):
        super(FabricException, self).__init__(*args, **kwargs)
