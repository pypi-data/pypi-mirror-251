from __future__ import annotations

import collections
import dataclasses
import typing
import warnings

from xsdata.formats.dataclass.models.generics import AnyElement

import momotor.bundles
from momotor.bundles.binding import MetaComplexType
from momotor.bundles.elements.base import Element
from momotor.bundles.exception import BundleFormatError
from momotor.bundles.typing.element import ElementMixinProtocol
from momotor.bundles.utils.arguments import BundleFactoryArguments, BundleConstructionArguments
from momotor.bundles.utils.filters import FilterableTuple

try:
    from typing import TypeAlias  # py3.10+
except ImportError:
    from typing_extensions import TypeAlias

try:
    from typing import Self  # py3.11+
except ImportError:
    from typing_extensions import Self

__all__ = ["default_generator", "Description", "Meta", "MetaMixin"]


CT = typing.TypeVar('CT', bound=object)


def default_generator() -> str:
    from momotor.bundles.version import __VERSION__
    return f'momotor-bundles {__VERSION__}'


class Description(Element[MetaComplexType.Description]):
    """ A Description element encapsulating :py:class:`~momotor.bundles.binding.momotor_1_0.MetaComplexType.Description`
    """
    __unset: typing.ClassVar = object()
    _lang: str | None = __unset
    _text: str | None = __unset

    @typing.final
    @property
    def lang(self) -> str | None:
        assert self._lang is not self.__unset, "Uninitialized attribute `lang`"
        return self._lang

    @lang.setter
    def lang(self, lang: str | None):
        assert self._lang is self.__unset, "Immutable attribute `lang`"
        assert lang is None or isinstance(lang, str)
        self._lang = lang

    @typing.final
    @property
    def text(self) -> str | None:
        assert self._text is not self.__unset, "Uninitialized attribute `content`"
        return self._text

    @text.setter
    def text(self, content: str | None):
        assert self._text is self.__unset, "Immutable attribute `content`"
        assert content is None or isinstance(content, str)
        self._text = content

    def create(self, *,
               text: str | None = None,
               lang: str | None = None) -> Self:
        self.text = text
        self.lang = lang
        return self

    def _clone(self, other: Self) -> Self:
        self.text = other.text
        self.lang = other.lang
        return self

    # noinspection PyMethodOverriding
    def recreate(self, target_bundle: "momotor.bundles.Bundle") -> "Description":
        """ Recreate this :py:class:`Description` in a target bundle.
        No attributes can be changed.

        :param target_bundle: The target bundle
        :return: The recreated :py:class:`Description`
        """
        return Description(target_bundle)._clone(self)

    def __convert_content(self, content: typing.Iterable, args: BundleFactoryArguments, warn: bool = True) \
            -> typing.Generator[str, None, None]:
        for item in content:
            if isinstance(item, AnyElement):
                msg = 'Incorrectly formatted meta-description. Use CDATA or escape HTML entities'
                if args.validate_xml and not args.legacy:
                    raise BundleFormatError(msg)
                elif warn:
                    warnings.warn(msg)
                    warn = False
                yield item.text
                yield from self.__convert_content(item.children, args, False)
            else:
                yield item

    def _create_from_node(self, node: MetaComplexType.Description, *,
                          args: BundleFactoryArguments) -> Self:
        self.text = ''.join(self.__convert_content(node.content, args))
        self.lang = node.lang
        return self

    def _construct_node(self, *, args: BundleConstructionArguments) -> MetaComplexType.Description:
        return MetaComplexType.Description(
            lang=self.lang,
            content=[self.text],
        )


NameType: TypeAlias = typing.Optional[str]
VersionType: TypeAlias = typing.Optional[str]
DescriptionsType: TypeAlias = typing.Sequence[Description]
AuthorsType: TypeAlias = tuple[str, ...]
SourcesType: TypeAlias = tuple[str, ...]
GeneratorsType: TypeAlias = tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class Meta:
    """ An frozen dataclass containing all meta-tag content. All fields are optional """

    #: `name` string - only a single name value is allowed. if the bundle has multiple names, the first one is used.
    name: NameType = dataclasses.field(default=None)

    #: `version` string - only a single version value is allowed. if the bundle has multiple versions, the first one is
    #: used.
    version: VersionType = dataclasses.field(default=None)

    #: a :py:class:`~momotor.bundles.utils.filters.FilterableTuple` of
    #: :py:class:`~momotor.bundles.elements.meta.Description` elements.
    descriptions: DescriptionsType = dataclasses.field(default_factory=FilterableTuple)

    #: a sequence of author strings.
    authors: AuthorsType = dataclasses.field(default_factory=tuple)

    #: a sequence of source strings.
    #: indicates the source of the bundle
    sources: SourcesType = dataclasses.field(default_factory=tuple)

    #: a sequence of generator strings.
    #: indicates the tool that created the bundle
    generators: GeneratorsType = dataclasses.field(default_factory=tuple)


class MetaMixin:
    """ A mixin class for elements with a `meta` attribute
    """
    __unset: typing.ClassVar = object()
    _meta: Meta = __unset

    @typing.final
    @property
    def meta(self) -> Meta:
        """ `meta` attribute """
        assert self._meta is not self.__unset, "Uninitialized attribute `meta`"
        return self._meta

    @meta.setter
    def meta(self, meta: Meta | None):
        assert self._meta is self.__unset, "Immutable attribute `meta`"
        if meta is not None:
            assert isinstance(meta, Meta), "Invalid type for attribute `meta`"
            self._meta = meta
        else:
            self._meta = Meta()

    def _collect_meta(self: ElementMixinProtocol, parent: object, *, args: BundleFactoryArguments) -> Meta:
        name: NameType | None = None
        version: VersionType | None = None
        authors: typing.MutableSequence[str] = collections.deque()
        descriptions: typing.MutableSequence[Description] = collections.deque()
        sources: typing.MutableSequence[str] = collections.deque()
        generators: typing.MutableSequence[str] = collections.deque()

        for meta in getattr(parent, 'meta'):
            meta = typing.cast(MetaComplexType, meta)

            names = meta.name
            if names:
                if len(names) > 1 or name is not None:
                    warnings.warn("Multiple `meta.name` elements, using first one")
                if name is None:
                    name = names[0]

            versions = meta.version
            if versions:
                if len(versions) > 1 or version is not None:
                    warnings.warn("Multiple `meta.version` elements, using first one")
                if version is None:
                    version = versions[0]

            authors.extend(meta.author)
            # noinspection PyProtectedMember
            descriptions.extend(
                Description(self.bundle)._create_from_node(d, args=args)
                for d in meta.description
            )
            sources.extend(meta.source)
            generators.extend(meta.generator)

        return Meta(
            name=name,
            version=version,
            descriptions=FilterableTuple(descriptions),
            authors=tuple(authors),
            sources=tuple(sources),
            generators=tuple(generators),
        )

    def _construct_meta_node(self, *, args: BundleConstructionArguments) \
            -> typing.Generator[MetaComplexType, None, None]:
        meta = self.meta

        name = [meta.name] if meta.name is not None else []
        version = [meta.version] if meta.version is not None else []
        author = list(meta.authors)
        # noinspection PyProtectedMember
        description = [d._construct_node(args=args) for d in meta.descriptions]
        source = list(meta.sources)
        generator = list(meta.generators)

        if args.generator_name:
            default_generator_name = default_generator()

            if isinstance(args.generator_name, str):
                generator_name = f'{args.generator_name} ({default_generator_name})'
            else:
                generator_name = default_generator_name

            if generator_name not in generator:
                generator.append(generator_name)

        if name or version or author or description or source or generator:
            yield MetaComplexType(
                name=name,
                version=version,
                author=author,
                description=description,
                source=source,
                generator=generator,
            )
