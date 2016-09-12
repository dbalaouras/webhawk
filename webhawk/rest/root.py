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
                "bitbucketwebhook": {
                    "href": flask.url_for('api.bitbucket', _external=True)
                },
                "githubwebhook": {
                    "href": flask.url_for('api.github', _external=True)
                },
                "gitlabwebhook": {
                    "href": flask.url_for('api.gitlab', _external=True)
                }
            }
        }

        return api_index
