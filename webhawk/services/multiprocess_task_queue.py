# Import standard python libs
import os
from Queue import Empty
from multiprocessing import Queue

from rest.api_errors import QueueFullException

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Stek.io"
__version__ = "0.0.1"
__status__ = "Prototype"
__abs_dirpath__ = os.path.dirname(os.path.abspath(__file__))


class MultiprocessTaskQueue(object):
    """
    Abstraction of the task queue using Python's multiprocessing Queue
    """

    def __init__(self, context):
        """
        Class initialization/constructor

        :param context: Application Context
        """

        # Initialize properties
        self._logger = context.get("logger")
        self._queue = Queue(maxsize=context["config"]["task_queue_size"])

        self._logger.debug("Initializing Multiprocess TaskQueue")

    def put(self, task):
        """
        Push one object to the queue

        :param task: The task t push to the queue
        :return: True if the task was added; false otherwise
        """
        # TODO: validate the task
        if self._queue.full():
            raise QueueFullException("Task Queue is full; cannot accept more tasks.")
        else:
            self._queue.put_nowait(task)

    def peek(self, block=True, timeout=None):
        """
        Pull one task from the queue

        :return: A task item
        """
        item = None
        try:
            item = self._queue.get(block=block, timeout=timeout)
        except Empty:
            pass

        return item

    def qsize(self):
        """
        Counts the items in the queue
        :return: The number of items in the queue
        """
        queue_length = None
        try:
            queue_length = self._queue.qsize()
        except NotImplementedError:
            # Raised in OSX :-(
            pass

        return queue_length

    def is_full(self):
        """
        Checks whether the queue is full or not.
        :return: True if the queue is full, False otherwise.
        """

        return self._queue.full()
