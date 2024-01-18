from __future__ import annotations

import typing

import momotor.bundles
from momotor.bundles.binding import PropertyComplexType, PropertiesComplexType
from momotor.bundles.elements.base import Element
from momotor.bundles.elements.content import ContentFullElement, NoContent
from momotor.bundles.elements.wildcard import WildcardAttrsMixin
from momotor.bundles.typing.element import ElementMixinProtocol
from momotor.bundles.utils.assertion import assert_elements_instanceof
from momotor.bundles.utils.arguments import BundleConstructionArguments, BundleFactoryArguments
from momotor.bundles.utils.filters import FilterableTuple
from momotor.bundles.utils.grouping import group_by_attr
from momotor.bundles.utils.nodes import get_nested_complex_nodes

try:
    from typing import TypeAlias  # py3.10+
except ImportError:
    from typing_extensions import TypeAlias

try:
    from typing import Self  # py3.11+
except ImportError:
    from typing_extensions import Self

__all__ = ['Property', 'PropertiesType', 'PropertiesMixin']


class Property(
    ContentFullElement[PropertyComplexType, PropertiesComplexType],
    WildcardAttrsMixin[PropertyComplexType],
):
    """ A Property element encapsulating :py:class:`~momotor.bundles.binding.momotor_1_0.PropertyComplexType`
    """
    __unset: typing.ClassVar = object()
    _accept: str | None = __unset

    @typing.final
    @property
    def accept(self) -> str | None:
        assert self._accept is not self.__unset, "Uninitialized attribute `accept`"
        return self._accept

    @accept.setter
    def accept(self, accept: str | None):
        assert self._accept is self.__unset, "Immutable attribute `accept`"
        assert accept is None or isinstance(accept, str)
        self._accept = accept

    @staticmethod
    def get_node_type() -> type[PropertyComplexType]:
        return PropertyComplexType

    @staticmethod
    def _get_parent_type() -> type[PropertiesComplexType]:
        return PropertiesComplexType

    # noinspection PyShadowingBuiltins
    def create(self, *,
               name: str,
               value: typing.Any = None,
               type_: str | None = None,
               accept: str | None = None,
               attrs: typing.Mapping[str, str] | None = None) -> Self:

        self._create_content(name=name, value=value, type_=type_)

        self.accept = accept
        self.attrs = attrs

        return self

    def _clone(self, other: Self, name: str | None) -> Self:
        self._clone_content(other, name=name)
        self.accept = other.accept
        self.attrs = other.attrs
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", *, name: str | None = None) -> "Property":
        """ Recreate this :py:class:`Property` in a target bundle, optionally changing the `name`.
        All other attributes are copied unchanged.

        :param target_bundle: The target bundle
        :param name: New name for the option
        :return: The recreated :py:class:`Property`
        """
        return Property(target_bundle)._clone(self, name)

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: PropertyComplexType,
                          parent: PropertiesComplexType,
                          ref_parent: PropertiesComplexType | None, *,
                          args: BundleFactoryArguments) -> Self:
        self._check_node_type(node)
        self._check_parent_type(parent)
        self._check_parent_type(ref_parent, True)

        super()._create_content_from_node(node, parent, ref_parent, args=args)
        super()._create_attrs_from_node(node, args=args)

        self.accept = node.accept

        return self

    def _construct_node(self, *, args: BundleConstructionArguments) -> PropertyComplexType:
        return (
            self._construct_attrs(
                self._construct_content(
                    PropertyComplexType(
                        accept=self.accept,
                    ),
                    args=args
                ),
                args=args
            )
        )


if Property.__doc__ and Element.__doc__:
    Property.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])


PropertiesType: TypeAlias = FilterableTuple[Property]


_no_default = object()


# noinspection PyProtectedMember
class PropertiesMixin:
    __unset: typing.ClassVar = object()
    _properties: PropertiesType = __unset
    _properties_by_name: dict[str, PropertiesType] | None = None

    @typing.final
    @property
    def properties(self) -> PropertiesType:
        """ `properties` children """
        assert self._properties is not self.__unset, "Uninitialized attribute `properties`"
        return self._properties

    @properties.setter
    def properties(self: ElementMixinProtocol | Self, properties: typing.Iterable[Property | None]):
        assert self._properties is self.__unset, "Immutable attribute `properties`"
        if properties:
            self._properties = assert_elements_instanceof(FilterableTuple(properties), Property, self.bundle)
        else:
            self._properties = PropertiesType()

        self._properties_by_name = None

    def _collect_properties(self: ElementMixinProtocol, parent: object, *,
                            args: BundleFactoryArguments) -> typing.Generator[Property, None, None]:
        properties_node: PropertiesComplexType | None = None
        for tag_name, node in get_nested_complex_nodes(parent, 'properties', 'property'):
            if tag_name == 'properties':
                properties_node = typing.cast(PropertiesComplexType, node)
            else:
                property_node = typing.cast(PropertyComplexType, node)
                yield Property(self.bundle)._create_from_node(property_node, properties_node, None, args=args)

    # noinspection PyMethodMayBeStatic
    def _construct_properties_nodes(self, *, args: BundleConstructionArguments) \
            -> typing.Generator[PropertiesComplexType, None, None]:
        properties = self.properties
        if properties:
            yield PropertiesComplexType(property=[
                      prop._construct_node(args=args)
                      for prop in properties
                  ])

    def get_properties(self, name: str) -> PropertiesType:
        """ Get properties

        :param name: `name` of the properties to get
        :return: A list of all matching properties.
        """
        if self._properties_by_name is None:
            self._properties_by_name = group_by_attr(self._properties, 'name')

        return self._properties_by_name[name]

    def get_property_value(self, name: str, *, default=_no_default) -> typing.Any:
        """ Get the value for a single property.
        If multiple properties match, the value of the first one found will be returned

        :param name: `name` of the property to get
        :param default: default value in case property is empty or undefined
        :return: The property value
        """
        try:
            return self.get_properties(name)[0].value

        except (NoContent, KeyError):
            if default is not _no_default:
                return default
            raise
