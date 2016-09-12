import datetime

from flask import request
from flask_restful import fields, marshal_with

from base_resource import BaseResource
from rest.api_errors import MethodNotAllowedException

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."


class WebHookBase(BaseResource):
    """
    RESTful Resource implementation for Recipes
    """
    resource_name = None

    resource_paths = ['/webhooks/{0}', '/webhooks/{0}/', '/webhooks/{0}/<string:resource_id>',
                      '/webhooks/{0}/<string:resource_id>/']

    resource_fields = {
        "id": fields.String,
        "status": fields.String,
        "timestamp": fields.DateTime,
        "request": fields.Raw
    }

    def get(self, resource_id=None):
        """
        Prevent READing this Resource (it's POST-only)

        :param resource_id: The resource Id
        """
        raise MethodNotAllowedException("GET not allowed in this Resource")

    def create_task(self, input):
        """
        Creates a new task parsing the inpug; must be implemented by child classes
        :return: The newly created task
        """
        return None

    @marshal_with(resource_fields)
    def post(self):
        """
        Responds to incoming HTTP POST requests
        """

        # Parse input
        json_data = request.get_json(force=True)

        # Construct the new task
        new_task = self.create_task(json_data)

        # Construct the response
        response = {
            "id": None,
            "status": "started",
            "timestamp": datetime.datetime.now(),
            "request": json_data,
            "created_task": new_task
        }

        return response, 202
