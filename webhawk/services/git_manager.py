# Import standard python libs

from fabric.operations import run

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Stek.io"


class GitManager(object):
    """
    Handles callbacks for the git VCS system.
    """

    def __init__(self, context):
        """
        Class initialization/constructor

        :param logger: An optional python logger; if None is passed, this worker will create one of its own.
        """

        # Initialize properties
        self._logger = context.get("logger")
        self._logger.info("Initializing Git VCS Managers")

    def clone(self, url, branch, target_path):
        """
        Checkout the repository
        :param branch: The branch to checkout

        """
        self._logger.info("Checking out code from '%s' to %s" % (url, target_path))
        run('git clone -b %s %s %s' % (branch, url, target_path))
