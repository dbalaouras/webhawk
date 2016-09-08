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
        env.warn_only = True
        env.use_ssh_config = True

        # Initialize properties
        self._context = context
        self._logger = context.get("logger")
        self._builder_hostname = context["config"]["builder_hostname"]
        self._workspace_path = context["config"]["workspace_path"]
        self._logger.info("Initializing Builder")

        # Use local fabric commands when the builder is localhost
        if self._builder_hostname == "localhost":
            self._change_dir = lcd
            self._run_command = local
        else:
            self._change_dir = cd
            self._run_command = run

    def run(self, build_id, repository_name, branch_name):
        """

        :param build_id: A unique build Id
        :param repository_name: The name of the repository to build
        :param branch_name: The name of the branch to build
        :return:
        """

        # Check if we have a recipe for the given repository
        recipe = self._context["recipe_repository"].find_by_name_and_branch(name=repository_name, branch=branch_name)

        # Check if we have dependencies and process them
        # # TODO: check for circular dependencies
        app_dependencies = recipe.get("dependencies", None)
        if app_dependencies:
            for dependency in app_dependencies:
                self.run(repository_name=dependency['repository'], branch_name=dependency['branch'], build_id=build_id)

        # Create build path
        build_base_path = self._get_build_base_path(build_id=build_id)
        build_path = "%s/%s" % (build_base_path, recipe["repository"]["name"])

        with settings(host_string=self._builder_hostname), self._change_dir(self._workspace_path):
            self._prepare(build_path=build_path)
            self._checkout(recipe=recipe, build_path=build_path)
            self._build(recipe=recipe, build_path=build_path)

            # Cleanup build directory if instructed
            if self._context["config"]["cleanup_builds"]:
                self._cleanup(build_base_path=build_base_path)

    def _get_build_base_path(self, build_id):
        """
        Constructs a build path
        :return: The build path
        """
        if self._workspace_path[0] != "/":
            # We have a relative path; lets make it absolute for clarity
            current_path = os.getcwd() if self._builder_hostname == "localhost" else self._run_command('pwd')
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
        self._run_command('[[ -d "{0}" ]] || mkdir -p {0}'.format(build_path))

    def _checkout(self, recipe, build_path):
        """
        Checkout the repository
        """
        cms_manager = self._context.get("%s_manager" % recipe["repository"]["vcs"], None)
        cms_manager.clone(url=recipe["repository"]["url"], branch=recipe["repository"]["branch"],
                          target_path=build_path, run_cmd=self._run_command)

    def _build(self, recipe, build_path):
        """
        Build the repository
        """
        self._logger.info("Building %s:%s on %s with command: '%s'" % (
            recipe["repository"]["name"], recipe["repository"]["branch"], build_path, recipe["command"]))

        if recipe.get("command", None):
            with self._change_dir(build_path):
                self._run_command("echo $PATH")
                self._run_command("%s" % (recipe["command"]))

        self._logger.info("Finished building")

    def _cleanup(self, build_base_path):
        """
        Cleanup after the build
        """
        self._logger.info("Removing build diretory '%s'" % build_base_path)
        self._run_command('rm -rf %s' % build_base_path)

    @classmethod
    def generate_build_id(cls):
        """
        Generates random build Ids
        :return: The generated build id
        """
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
