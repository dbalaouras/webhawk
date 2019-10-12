from rest.api_errors import InvalidUsage
from rest.github_webhook import GithubWebHook

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."


class GitlabWebHook(GithubWebHook):
    """
    RESTful Resource for the Gitlab Webhook
    """
    resource_name = "gitlab"

    def create_task(self, payload):
        """
        Creates a new build task using the input (usually a POST Payload)
        :param payload: The task payload
        :return: The newly created task
        """

        # Get the task manager
        task_manager = self._context.get("task_manager")

        try:
            repository_name = payload['repository']['name']
            branch_name = payload['ref'].split('/')[2]
            vcs = "git"
        except KeyError:
            raise InvalidUsage("Invalid payload: %s" % str(payload))

        # Construct the new task
        new_task = task_manager.create_new_task(repository_name=repository_name, branch_name=branch_name, vcs=vcs)

        return new_task
