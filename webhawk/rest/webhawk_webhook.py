from rest.api_errors import InvalidUsage
from rest.webhook_base import WebHookBase

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."


class WebHawkWebHook(WebHookBase):
    """
    RESTful Resource for the Github Webhook
    """
    resource_name = "webhawk"

    def create_task(self, payload):
        """
        Creates a new build task using the input (usually a POST Payload)
        """

        # Get the task manager
        task_manager = self._context.get("task_manager")

        # Process the input
        try:
            repository_name = payload['repository']
            branch_name = payload['branch']
            vcs = payload['scm']
            recipe_id = payload.get('recipe_id', None)
        except KeyError:
            raise InvalidUsage("Invalid payload: %s" % str(payload))

        # Construct the new task
        new_task = task_manager.create_new_task_by_id(recipe_id=recipe_id)

        return new_task
