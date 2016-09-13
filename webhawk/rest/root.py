import flask

from rest.base_resource import BaseResource

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."


class Root(BaseResource):
    """
    The Artist RESTful Resource
    """

    resource_paths = ['', '/']
    resource_name = "root"
    resource_fields = {}

    def get(self, resource_id=None):
        """
        Responds to HTTP GET method
        :return: A dictionary with Resource data
        """
        api_index = {
            "_links": {
                "recipe": {
                    "href": flask.url_for('api.recipe', _external=True)
                },
                "bitbucket-webhook": {
                    "href": flask.url_for('api.bitbucket', _external=True)
                },
                "github-webhook": {
                    "href": flask.url_for('api.github', _external=True)
                },
                "gitlab-webhook": {
                    "href": flask.url_for('api.gitlab', _external=True)
                },
                "webhawk-webhook": {
                    "href": flask.url_for('api.webhawk', _external=True)
                }
            }
        }

        return api_index
