from rest.api_errors import InvalidUsage
from rest.webhook_base import WebHookBase

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."


class BitBucketWebHook(WebHookBase):
    """
    RESTful Resource for the Bitbucket Webhook
    """
    resource_name = "bitbucket"

    def create_task(self, payload):
        """
        Creates a new build task using the input (usually a POST Payload)
        :param payload: The task payload
        :return: The newly created task

        """

        # Get the task manager
        task_manager = self._context.get("task_manager")

        # Process the input
        try:
            repository_name = payload['repository']['name']
            branch_name = payload['push']['changes'][0]['new']['name']
            vcs = payload['repository']['scm']
        except KeyError:
            raise InvalidUsage("Invalid payload: %s" % str(payload))

        # Construct the new task
        new_task = task_manager.create_new_task(repository_name=repository_name, branch_name=branch_name, vcs=vcs)

        return new_task
