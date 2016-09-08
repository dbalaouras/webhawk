import os
from multiprocessing import Process

from rest.api_errors import NotImplementedException, ServiceUnavailableException
from services.builder import Builder

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."


class BuildTaskManager(object):
    """
    Spawns build workers and distributes build tasks.
    """

    def __init__(self, context):
        """
        Class initialization/constructor

        :param context: The app context; provides access to singleton services (e.g. logger, task_queue)
        """

        # Store input
        self._context = context
        self._task_queue = context["task_queue"]
        self._logger = context["logger"]

    def create_new_task(self, repository_name, branch_name, vcs):
        """
        Create a new task  object

        :param repository_name: The repository name
        :param branch_name: The branch name to checkout
        :param vcs: The Version Control System used by the remote repository
        :return: The newly created Task
        """

        # TODO: Validate input

        # Check if we have a recipe for the given repository
        recipe = self._context["recipe_repository"].find_by_name_and_branch(name=repository_name, branch=branch_name)

        if not recipe:
            raise ServiceUnavailableException(
                "Could not find build recipe for repository '%s' and branch '%s'" % (repository_name, branch_name))

        vcs_manager = self._context.get("%s_manager" % recipe["repository"]['vcs'], None)

        if not vcs_manager:
            raise NotImplementedException("VCS system '%s' is currently not supported." % vcs)

        new_task = {
            "repository_name": repository_name,
            "branch_name": branch_name,
            "vcs": vcs
        }

        # Put task queue
        self._context["task_queue"].put(new_task)

        return new_task

    def start_workers(self, workers_num=1):
        """
        Start build workers

        :param workers_num: How many workers to start
        :return:
        """
        self._logger.info("Starting %s Task Workers" % workers_num)
        reader_p = Process(target=self._listen)
        reader_p.daemon = True
        reader_p.start()

    def _listen(self):
        """
        Implements the queue listener callback.
        """
        self._logger.info("Worker with PID '%s' started" % os.getpid())
        while True:
            self._logger.debug("Listening to the task queue for %s" % 10)
            item = self._task_queue.peek(timeout=10)
            if item:
                self._logger.debug("Picked item: %s" % item)
                build_id = Builder.generate_build_id()
                self._context.get("builder").run(build_id=build_id, repository_name=item["repository_name"],
                                                 branch_name=item["branch_name"])
