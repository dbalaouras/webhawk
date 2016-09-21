from flask_restful import fields

from base_resource import BaseResource

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."


class Recipe(BaseResource):
    """
    RESTful Resource implementation for Recipes
    """
    resource_name = "recipe"

    resource_fields = {
        "id": fields.String,
        "repository": fields.Nested({
            "name": fields.String,
            "branch": fields.String,
            "url": fields.String,
            "vcs": fields.String
        }),
        "command": fields.String,
        "dependencies": fields.List(
            fields.Nested({
                "repository": fields.String,
                "branch": fields.String
            })
        )
    }

    def _get_single_resource(self, resource_id):
        """
        Get a Resource given it's identifier
        :param resource_id: The Resource identifier
        :return: The Resource (can be None if not found)
        """
        return self._context["recipe_repository"].find_one(id=resource_id)

    def _get_resource_collection(self, size, page):
        """
        Get a paged collection of Resource entities

        :param size: The size of the page
        :param page: the number of the page
        :return: A page of the Resource entities
        """

        return self._context["recipe_repository"].find_all()

    def _get_total_entities_size(self):
        """
        Gets the total number of Resource Entities
        """
        return self._context["recipe_repository"].count()
