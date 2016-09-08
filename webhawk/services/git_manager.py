# Import standard python libs

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

    def clone(self, url, branch, target_path, run_cmd):
        """
        Checkout the repository`
        :param url: URL to clone
        :param branch: The branch to checkout
        :param target_path: The target path of the cloning
        :param run_cmd: The command execution function

        """
        self._logger.info("Checking out code from '%s' to %s" % (url, target_path))
        run_cmd('git clone -b %s %s %s' % (branch, url, target_path))
