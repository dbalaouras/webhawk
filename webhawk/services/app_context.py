__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."

# Do not modify the following
__default_feature_name__ = "DO_NOT_MODIFY"


class AppContext(object):
    """
    App Context based on Service Locator Pattern
    """

    def __init__(self, allow_replace=False):
        """

        :param allow_replace: Allow replace of the feature
        """
        self.providers = {}
        self.allow_replace = allow_replace

    def register(self, feature, provider, *args, **kwargs):
        if not self.allow_replace:
            assert not self.providers.has_key(feature), "Duplicate feature: %r" % feature
        if callable(provider):
            def call():
                return provider(*args, **kwargs)
        else:
            def call():
                return provider
        self.providers[feature] = call

    def __getitem__(self, feature):
        try:
            provider = self.providers[feature]
        except KeyError:
            raise KeyError("Unknown feature named %r" % feature)
        return provider()

    def get(self, feature, default=__default_feature_name__):
        """
        Wrapper of __getitem__ method
        :param feature: The Feature registered within the WebHawk Context
        :param default: Default return value
        :return: The reference to the implementation of the requested feature; None otherwise
        """

        feature_impl = default
        if default == __default_feature_name__:
            # Will raise an exception if feature is not implemented
            feature_impl = self.__getitem__(feature)
        else:
            try:
                feature_impl = self.__getitem__(feature)
            except KeyError:
                pass

        return feature_impl
