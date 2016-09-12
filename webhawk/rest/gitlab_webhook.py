from rest.github_webhook import GithubWebHook

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."


class GitlabWebHook(GithubWebHook):
    """
    RESTful Resource for the Gitlab Webhook
    """
    resource_name = "gitlab"
