import math

import flask
from flask_restful import fields, Resource, marshal_with
from flask_restful import reqparse

from rest.api_errors import ResourceNotFoundException

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Dimi Balaouras - Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."


class BaseResource(Resource):
    """
    Abstract Base of WebHawk's RESTful Resources.

    This class abstracts generating RESTful Resources and formatting them using the HAL format
    (see http://stateless.co/hal_specification.html)

    """

    # Define basic pattern for the Resource URl. The parameter {0} is replaced by the API's base path,
    # and {1} with the resource name. Can be overriden by Resource subclasses
    resource_paths = ['/{0}', '/{0}/', '/{0}/<string:resource_id>']

    # Resource properties that must be overridden by subclasses
    resource_name = None
    resource_fields = None

    def __init__(self, context):
        """
        Resource initializer.
        """

        # Store input
        self._context = context
        self._logger = context["logger"]

        # Generate Resource URL
        self._resource_base_url = flask.url_for("api.%s" % self.resource_name, _external=True)

        # Generate Resource field definitions
        self._resource_list_fields = self._get_resource_list_fields()
        self._add_default_fields()
        self._add_default_collection_fields()

    @classmethod
    def add_resource_to_api(cls, api, context):
        """

        Adds the current Resource to the given flask-restful API. Must be called for subclasses of this class.
        :param api: The Flask-RESTful API object
        :param context: WebHawk Services Context
        """
        formatted_paths = [path.format(cls.resource_name).replace("//", "/") for path in cls.resource_paths]
        api.add_resource(cls, *formatted_paths, endpoint=cls.resource_name, resource_class_kwargs={"context": context})

    def get(self, resource_id=None):
        """
        Responds to HTTP GET method
        :param resource_id: (optional) the Id of the Resource to retrieve. If no resource_id is given,
                            a resource collection is returned.
        """

        @marshal_with(self.resource_fields)
        def get_single_resource():
            """
            Wrapper of the _get_single method, using the marshal_with decorator
            """
            resource = self._get_single_resource(resource_id=resource_id)
            if not resource:
                raise ResourceNotFoundException("The Resource with Id '%s' was not found" % resource_id)

            return resource

        @marshal_with(self._resource_list_fields)
        def get_resource_collection():
            """
            Wrapper of the get_list method, using the marshal_with decorator
            """

            # Count total documents
            total_documents = self._get_total_entities_size()

            # Extract paging parameters
            parser = reqparse.RequestParser()
            parser.add_argument('size', type=int, required=False,
                                help="Sets the size of this collection page.")
            parser.add_argument('page', type=int, required=False, help='Defines the number of the page')
            args = parser.parse_args()

            # Calculate paging variables
            size = 20 if args["size"] is None or args["size"] > 200 else args["size"]
            page = 0 if args["page"] is None else args["page"]

            # Get list of resources
            resources = self._get_resource_collection(size if size < 200 else 20, page)
            resources_list = map(self._post_process_entity, resources) if resources else []

            # Construct Resource links
            current_url = "%s?page=%s&size=%s" % (self._resource_base_url, page, size)
            next_url = "%s?page=%s&size=%s" % (self._resource_base_url, page + 1, size) if (
                                                                                               page + 1) * size <= total_documents else None
            prev_url = "%s?page=%s&size=%s" % (self._resource_base_url, page - 1, size) if (
                                                                                               page - 1) * size >= 0 else None

            # Create Resource
            list_resource = {
                "_embedded": {self.resource_name: list(resources_list)},
                "_links": {"self": {"href": current_url}},
                "_page": {
                    "page": page,
                    "size": len(resources_list),
                    "next": next_url,
                    "prev": prev_url,
                    "total_resources": total_documents,
                    "total_pages": math.floor(total_documents / size) + 1
                }
            }

            return list_resource

        return get_single_resource() if resource_id is not None else get_resource_collection()

    def _get_single_resource(self, resource_id):
        """

        :param resource_id: The id of the Resource
        :return: The Resource object as dictionary
        """
        return None

    def _get_resource_collection(self, size, page):
        """

        :param size: Size of the Page
        :param page: Page number
        :return: A collection of Resources (as dictionaries)
        """
        return None

    def _get_total_entities_size(self):
        """
        Get the total number of Resources
        :return: The total number of Resources
        """
        return 0

    def _get_resource_list_fields(self):
        """
        Returns a list of flask-restful fields for a single Resource
        """
        res_fields = {
            "_links": fields.Nested({"self": fields.Nested({"href": fields.String})}),
            "_embedded": fields.Nested({self.resource_name: fields.Nested(self.resource_fields)})
        }
        return res_fields

    def _post_process_entity(self, entity):
        """
        Processes entity before formatting it

        :param entity: The Entity to process
        :return: The processed Entity
        """
        self._attach_self_link(entity)
        return entity

    def _attach_self_link(self, entity):
        """
        Adds a "self" link to the given Resource
        :param entity:
        :return:
        """
        entity["_links"] = {
            "self": {"href": "%s/%s" % (self._resource_base_url, entity.get("id", 0))}
        }
        return entity

    def _add_default_fields(self):
        """
        Adds default fields to Resources

        :return:
        """
        self.resource_fields["_links"] = fields.Nested({"self": fields.Nested({"href": fields.String})})
        self.resource_fields["id"] = fields.String

    def _add_default_collection_fields(self):
        """
        Adds default fields to Resource Collections

        :return:
        """

        self._resource_list_fields["_page"] = fields.Nested({
            "page": fields.Integer,
            "size": fields.Integer,
            "total_elements": fields.Integer,
            "total_pages": fields.Integer,
            "next": fields.String,
            "prev": fields.String
        })
