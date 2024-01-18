import typing

from momotor.bundles import Bundle
from momotor.bundles.elements.content import ContentFullElement, ContentBasicElement
from momotor.bundles.utils.arguments import BundleConstructionArguments


class TestElementMixin:
    def create(self, **kwargs) -> typing.NoReturn:
        raise NotImplementedError

    def recreate(self, target_bundle: Bundle) -> typing.NoReturn:
        raise NotImplementedError

    def _create_from_node(self, node: typing.Any, *, args: BundleConstructionArguments) -> typing.NoReturn:
        raise NotImplementedError

    def _construct_node(self, *, args: BundleConstructionArguments) -> typing.NoReturn:
        raise NotImplementedError

    def _get_parent_type(self) -> typing.NoReturn:
        raise NotImplementedError


class TestBundle(TestElementMixin, Bundle):
    """ A :py:class:`~momotor.bundles.Bundle` for use in unit tests.

    The abstract methods are implemented as methods that raise :py:exc:`NotImplementedError`, making it
    impossible to instantiate this class during tests.
    """
    @staticmethod
    def get_default_xml_name() -> typing.NoReturn:
        raise NotImplementedError

    @staticmethod
    def get_category() -> typing.NoReturn:
        raise NotImplementedError


class TestContentFullElement(TestElementMixin, ContentFullElement):
    """ A :py:class:`~momotor.bundles.elements.content.ContentFullElement` for use in unit tests.

    The abstract methods are implemented as methods that raise :py:exc:`NotImplementedError`, making it
    impossible to instantiate this class during tests.
    """
    pass


class TestContentBasicElement(TestElementMixin, ContentBasicElement):
    """ A :py:class:`~momotor.bundles.elements.content.ContentBasicElement` for use in unit tests.

    The abstract methods are implemented as methods that raise :py:exc:`NotImplementedError`, making it
    impossible to instantiate this class during tests.
    """
    pass
