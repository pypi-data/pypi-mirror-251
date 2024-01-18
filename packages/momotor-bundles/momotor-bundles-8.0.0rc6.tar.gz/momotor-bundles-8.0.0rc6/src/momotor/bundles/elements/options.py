from __future__ import annotations

import typing

import momotor.bundles
from momotor.bundles.binding import OptionComplexType, OptionsComplexType
from momotor.bundles.elements.base import Element
from momotor.bundles.elements.content import ContentFullElement, NoContent
from momotor.bundles.elements.refs import resolve_ref
from momotor.bundles.elements.wildcard import WildcardAttrsMixin
from momotor.bundles.typing.element import ElementMixinProtocol
from momotor.bundles.utils.arguments import BundleConstructionArguments, BundleFactoryArguments
from momotor.bundles.utils.assertion import assert_elements_instanceof
from momotor.bundles.utils.domain import split_domain, unsplit_domain, merge_domains
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

__all__ = ['Option', 'OptionsType', 'OptionsMixin']


class Option(
    ContentFullElement[OptionComplexType, OptionsComplexType],
    WildcardAttrsMixin[OptionComplexType],
):
    """ An Option element encapsulating :py:class:`~momotor.bundles.binding.momotor_1_0.OptionComplexType`
    """
    DEFAULT_DOMAIN: typing.ClassVar[str] = 'checklet'

    __unset: typing.ClassVar = object()

    _domain: str = __unset
    _domain_parts: tuple[str, str | None] = __unset
    _description: str | None = __unset

    @typing.final
    @property
    def domain(self) -> str:
        """ `domain` attribute """
        assert self._domain is not self.__unset, "Uninitialized attribute `domain`"
        return self._domain

    @domain.setter
    def domain(self, domain: str | None):
        assert self._domain is self.__unset, "Immutable attribute `domain`"
        assert domain is None or isinstance(domain, str), "Invalid type for attribute `domain`"

        self._domain = merge_domains(domain, self.DEFAULT_DOMAIN)
        self._domain_parts = split_domain(self._domain)

    @property
    def domain_parts(self) -> tuple[str, str | None]:
        """ A tuple with the two parts of the ``domain``.

        If ``domain`` equals `<main>#<sub>` this is (`<main>`, `<sub>`).
        If ``domain`` does not contain a ``#``, it equals (`<domain>`, None).
        """
        assert self._domain_parts is not self.__unset, "Uninitialized attribute `domain`"
        return self._domain_parts

    @typing.final
    @property
    def description(self) -> str | None:
        """ `description` attribute """
        assert self._description is not self.__unset, "Uninitialized attribute `description`"
        return self._description

    @description.setter
    def description(self, description: str | None):
        assert self._description is self.__unset, "Immutable attribute `description`"
        assert description is None or isinstance(description, str)
        self._description = description

    @staticmethod
    def get_node_type() -> type[OptionComplexType]:
        return OptionComplexType

    @staticmethod
    def _get_parent_type() -> type[OptionsComplexType]:
        return OptionsComplexType

    # noinspection PyShadowingBuiltins
    def create(self, *,
               name: str,
               domain: str | None = None,
               value: typing.Any = None,
               type_: str | None = None,
               description: str | None = None,
               attrs: typing.Mapping[str, str] | None = None) -> Self:

        self._create_content(name=name, value=value, type_=type_)

        self.domain = domain
        self.description = description
        self.attrs = attrs

        return self

    def _clone(self, other: Self, name: str | None, domain: str | None) -> Self:
        self._clone_content(other, name=name)
        self.domain = domain or other.domain
        self.description = other.description
        self.attrs = other.attrs
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", *, name: str | None = None, domain: str | None = None) \
            -> "Option":

        """ Recreate this :py:class:`Option` in a target bundle, optionally changing the `name` or `domain`.
        All other attributes are copied unchanged.

        :param target_bundle: The target bundle
        :param name: New name for the option
        :param domain: New domain for the option
        :return: The recreated :py:class:`Option`
        """
        return Option(target_bundle)._clone(self, name, domain)

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: OptionComplexType,
                          direct_parent: OptionsComplexType,
                          ref_parent: OptionsComplexType | None, *,
                          args: BundleFactoryArguments) -> Self:
        self._check_node_type(node)
        self._check_parent_type(direct_parent)
        self._check_parent_type(ref_parent, True)

        self._create_content_from_node(node, direct_parent, ref_parent, args=args)
        self._create_attrs_from_node(node, args=args)

        self.domain = merge_domains(
            node.domain,
            ref_parent.domain if ref_parent else direct_parent.domain,
            self.DEFAULT_DOMAIN
        )
        self.description = node.description

        return self

    def _construct_node(self, *, args: BundleConstructionArguments) -> OptionComplexType:
        domain_parts = self._domain_parts
        if domain_parts[0] == self.DEFAULT_DOMAIN:
            domain = unsplit_domain(None, domain_parts[1])
        else:
            domain = self._domain

        return (
            self._construct_attrs(
                self._construct_content(
                    OptionComplexType(
                        domain=domain,
                        description=self.description,
                    ),
                    args=args
                ),
                args=args
            )
        )


if Option.__doc__ and Element.__doc__:
    Option.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])


OptionsType: TypeAlias = FilterableTuple[Option]


_no_default = object()


# noinspection PyProtectedMember
class OptionsMixin:
    # noinspection PyUnresolvedReferences
    """ A mixin for Elements to implement options

    :ivar options: List of :py:class:`~momotor.bundles.options.Option` objects
    """
    __unset: typing.ClassVar = object()

    _options: OptionsType = __unset
    _options_by_domain_name: dict[tuple[str, str], OptionsType] | None = None

    @typing.final
    @property
    def options(self) -> OptionsType:
        """ `options` children """
        assert self._options is not self.__unset, "Uninitialized attribute `options`"
        return self._options

    @options.setter
    def options(self: ElementMixinProtocol | Self, options: typing.Iterable[Option] | None):
        assert self._options is self.__unset, "Immutable attribute `options`"
        if options is not None:
            self._options = assert_elements_instanceof(FilterableTuple(options), Option, self.bundle)
        else:
            self._options = OptionsType()

        self._options_by_domain_name = None

    def _collect_options(self: ElementMixinProtocol,
                         parent: object,
                         ref_parents: typing.Iterable[typing.Iterable[OptionsComplexType]], *,
                         args: BundleFactoryArguments) \
            -> typing.Generator[Option, None, None]:

        options_node: OptionsComplexType | None = None
        for tag_name, node in get_nested_complex_nodes(parent, 'options', 'option'):
            if tag_name == 'options':
                options_node = typing.cast(OptionsComplexType, node)
            else:
                option_node = typing.cast(OptionComplexType, node)
                if ref_parents:
                    ref_parent, option_node = resolve_ref('option', option_node, ref_parents)
                else:
                    ref_parent = None

                yield Option(self.bundle)._create_from_node(option_node, options_node, ref_parent, args=args)

    def _construct_options_nodes(self, *, args: BundleConstructionArguments) \
            -> typing.Generator[OptionsComplexType, None, None]:
        # TODO group by domain
        options_element = self.options
        if options_element:
            yield OptionsComplexType(option=[
                option._construct_node(args=args)
                for option in options_element
            ])

    def get_options(self, name: str, *, domain: str = Option.DEFAULT_DOMAIN) -> OptionsType:
        """ Get options

        :param name: `name` of the options to get
        :param domain: `domain` of the options to get. Defaults to "checklet"
        :return: A filterable tuple of all matching options.
        """
        if self._options_by_domain_name is None:
            self._options_by_domain_name = group_by_attr(self.options, 'domain', 'name')

        return self._options_by_domain_name[(domain, name)]

    def get_option_value(self, name: str, *, domain: str = Option.DEFAULT_DOMAIN, default=_no_default) -> typing.Any:
        """ Get the value for a single option.
        If multiple options match, the value of the first one found will be returned

        :param name: `name` of the option to get
        :param domain: `domain` of the option to get. Defaults to "checklet"
        :param default: default value in case option is empty or undefined
        :return: The option value
        """
        try:
            return self.get_options(name, domain=domain)[0].value

        except (NoContent, KeyError):
            if default is not _no_default:
                return default
            raise
