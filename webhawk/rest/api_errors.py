from flask import jsonify

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."


class ApiErrorRegistry(object):
    """
    Exception to API Error mapper and Error Handler Registrar
    """

    def __init__(self, logger):
        """
        Class initialization/constructor

        :param logger: An optional python logger; if None is passed, this worker will create one of its own.
        """

        # Initialize properties
        self._logger = logger

    @classmethod
    def register_error_handlers(cls, app):
        """
        Register error handlers to the given Flask App
        :param app: The Flask Application
        :return:
        """

        @app.errorhandler(GenericAPIError)
        def handle_invalid_usage(error):
            response = jsonify(error.to_dict())
            response.status_code = error.status_code
            return response

        @app.errorhandler(Exception)
        def handle_all_other_errors(error):
            """

            :param error:
            :return:
            """
            js = {
                "message": str(error),
                "error_code": 500
            }
            response = jsonify(js)
            response.status_code = 500
            return response


class GenericAPIError(Exception):
    """
    Invalid usage Error
    """
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['error_code'] = self.status_code
        return rv


class InvalidUsage(GenericAPIError):
    """
    Invalid usage Error
    """
    status_code = 400


class ResourceNotFoundException(GenericAPIError):
    """
    Resource Not Found Exception
    """
    status_code = 404


class ServiceUnavailableException(GenericAPIError):
    """
    For generic Service Unavailable exceptions
    """
    status_code = 503


class QueueFullException(GenericAPIError):
    """
    Invalid usage Error
    """
    status_code = 503


class NotImplementedException(GenericAPIError):
    """
    Not implemented Feature
    """
    status_code = 501


class MethodNotAllowedException(GenericAPIError):
    """
    Method not allowed exception
    """
    status_code = 405
