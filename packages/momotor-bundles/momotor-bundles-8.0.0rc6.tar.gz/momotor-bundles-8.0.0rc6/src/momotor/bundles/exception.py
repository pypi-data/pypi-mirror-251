class BundleError(Exception):
    """ Base class for all exceptions raised by the bundles module."""
    pass


class BundleHashError(BundleError):
    """ Raised when a bundle attachment hash does not match the attachment content.

    This is a subclass of :py:exc:`BundleError`.
    """
    pass


class BundleFormatError(BundleError):
    """ Raised when a bundle is not valid.

    This is a subclass of :py:exc:`BundleError`.
    """
    pass


class InvalidRefError(BundleFormatError):
    """ Raised when a `ref` attribute is invalid.

    This is a subclass of :py:exc:`BundleFormatError`.
    """
    pass


class InvalidBundle(BundleFormatError):
    """ Raised when a bundle is invalid.

    This is a subclass of :py:exc:`BundleFormatError`.
    """
    pass


class LxmlMissingError(BundleError):
    """ Raised when `lxml`_ is requested but not installed.

    This is a subclass of :py:exc:`BundleError`.
    """
    pass


class BundleLoadError(BundleError):
    """ Raised when a bundle cannot be loaded.

    This is a subclass of :py:exc:`BundleError`.
    """
    pass
