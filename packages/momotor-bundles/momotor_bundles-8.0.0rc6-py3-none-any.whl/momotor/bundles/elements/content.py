from __future__ import annotations

import typing
import warnings
from abc import ABC
from collections import deque
from decimal import Decimal
from io import BytesIO
from pathlib import PurePosixPath, Path, PurePath

from xsdata.formats.dataclass.models.generics import AnyElement
from xsdata.utils.namespaces import build_qname

from momotor.bundles.binding.momotor_1_0 import __NAMESPACE__
from momotor.bundles.elements.base import NestedElement, Element
from momotor.bundles.exception import BundleFormatError
from momotor.bundles.mixins.attachments import SrcAttachmentMixin, AttachmentSrc
from momotor.bundles.mixins.name import NameStrMixin, NamePathMixin
from momotor.bundles.utils.arguments import BundleConstructionArguments, BundleFactoryArguments
from momotor.bundles.utils.boolean import to_bool
from momotor.bundles.utils.encoding import decode_data, encode_data

try:
    from typing import TypeAlias  # py3.10+
except ImportError:
    from typing_extensions import TypeAlias

try:
    from typing import Self  # py3.11+
except ImportError:
    from typing_extensions import Self

__all__ = [
    'ContentBasicElement', 'ContentFullElement', 'ContentAttachmentElement',
    'NO_CONTENT', 'ContentBasicProcessedType',
    'NoContent', 'AttachmentContent',
]


def is_printable(s: str) -> bool:
    return all((32 <= ord(c) < 127 or ord(c) >= 160) for c in s)


VALUE_TYPE_MAP = {
    'string': str,
    'integer': int,
    'float': float,
    'boolean': to_bool,
}

ALTERNATE_VALUE_TYPES = {
    'int': 'integer',
    'bool': 'boolean',
}

PT = typing.TypeVar('PT', bound=object)
CT = typing.TypeVar('CT', bound=object)
PCT = typing.TypeVar('PCT', bound=object)

true_qname = build_qname(__NAMESPACE__, 'true')
false_qname = build_qname(__NAMESPACE__, 'false')
none_qname = build_qname(__NAMESPACE__, 'none')

NoContentType = typing.NewType('NoContentType', object)
ContentBasicProcessedType: TypeAlias = typing.Union[str, bool, None, NoContentType]
ContentFullProcessedType: TypeAlias = typing.Union[ContentBasicProcessedType, bytes, int, float, Decimal]
RawType: TypeAlias = typing.Union[str, bool, None]

#: A sentinel value indicating there is no content.
NO_CONTENT = NoContentType(object())


class NoContent(ValueError):
    """ Raised when no content was provided. Subclass of :py:exc:`ValueError` """
    pass


class AttachmentContent(ValueError):
    """ Raised when the content is in an attachment. Subclass of :py:exc:`ValueError` """
    pass


class ContentElementBase(typing.Generic[CT, PCT, PT], NestedElement[CT, PCT], NameStrMixin, ABC):
    """ Base class for elements with content, either as a value attribute, child nodes or as an attachment.
    Handles `name`, `type`, `value` and `encoding` attributes and child node content.
    This unifies the handling of <option>, <property> and <file> nodes

    The subclasses :py:class:`ContentBasicElement`, :py:class:`ContentFullElement` and
    :py:class:`ContentAttachmentElement` exist mainly to create the proper documentation of the properties and methods.

    `value` attribute, attachments and child nodes with content are mutually exclusive.
    `type` has a double role: For nodes with a 'value' attribute it indicates the type (string, integer or float),
    for nodes with child content or attachment, it is the content mime type.
    `encoding` is only used with child content, supported encodings are ``base64`` and ``quopri``
    """
    HAS_ENCODING: typing.ClassVar
    VALID_PROCESSED_TYPES: typing.ClassVar
    MAX_VALUE_LENGTH: typing.ClassVar = 1000

    # _src: PurePosixPath | None = None  # The src attribute
    _value: str | None = None  # The value attribute
    _encoding: str | None = None  # The encoding attribute
    _content_set: bool = False  # Content has been provided

    _type: str | None = None
    _type_set: bool = False

    # Raw content is the content as it appears in the XML document, a sequence of str, bool or None items.
    #
    # Processed content is the content converted and decoded using the `type` and `encoding` attributes, a sequence
    # containing a single str, boolean or None.

    # Conversion from raw to processed content and vice versa is only done when required.

    # XML child content  encoding attr  Raw content         Processed content    Remark
    # -----------------  -------------  ------------------  -------------------  ---------
    # "string value"                    ("string value",)   ("string value",)    If content is printable, it's a `str`
    # "=00"              "quopri"       ("=00",)            (b"\00",)            Encoded/unprintable content is `bytes`
    # "AA=="             "base64"       ("AA==",)           (b"\00",)
    # <true/>                           (True,)             (True,)
    # <false/>                          (False,)            (False,)
    # <none/>                           (None,)             (None,)
    #
    # value attr  type attr  encoding attr  Raw content         Processed content
    # ----------  ---------  -------------  ------------------  ------------------------------
    # "string"    "string"                  (b"string",)        ("string",)
    # "1"         "int"                     (1,)                (1,)
    # "1.0"       "float"                   (1.0,)              (1.0,)
    #
    # Having both the value attribute set and child content is an unsupported. If XML documents contain this, the
    # `value` attribute is used and the child content is ignored during conversion to processed content.

    _raw_content: typing.Sequence[RawType] | None = None  # Raw unprocessed content
    _processed_value: typing.Sequence[PT] | None = None  # Processed content
    _content_type: str | None = None  # The child content

    @property
    def value(self) -> PT:
        """ `value` attribute: The content.

        Setting `value` to `None` will generate a node with a <none/> tag. Set value to
        :py:obj:`~momotor.bundles.elements.content.NO_CONTENT` to create an empty content node.

        When accessing, raises :py:exc:`~momotor.bundles.elements.content.NoContent` if no content was set instead
        of returning :py:obj:`~momotor.bundles.elements.content.NO_CONTENT`,
        raises :py:exc:`~momotor.bundles.elements.content.AttachmentContent` if the node refers to an attachment
        using the `src` attribute instead of having inline content.
        """
        assert self._content_set, "Content not set"
        value = self._process_value()[0]
        if value is NO_CONTENT:
            raise NoContent

        return value

    @value.setter
    def value(self, value: PT):
        assert not self._content_set, "Immutable attribute `value`"

        if not (value is None or value is NO_CONTENT or isinstance(value, self.VALID_PROCESSED_TYPES)):
            raise TypeError(f"Invalid type {type(value)} for attribute `value`, expected one of {self.VALID_PROCESSED_TYPES}")

        if not self.HAS_ENCODING and isinstance(value, str) and not is_printable(value):
            raise ValueError("This content cannot be encoded")

        self._value = None
        self._processed_value = None if value is NO_CONTENT else (value,)
        self._raw_content = None
        self._content_set = True

    def _set_type(self, type_: str | None):
        assert not self._type_set, "Immutable attribute `type`"
        assert type_ is None or isinstance(type_, str)

        self._type = type_
        self._type_set = True

    def _create_content(self, *, name: str | None = None, value: PT = NO_CONTENT) -> Self:
        """ Set content attributes directly

        :param name: name attribute
        :param value: value attribute
        """
        self.name = name
        self.value = value
        return self

    def _clone_content(self, other: Self, *, name: str | None = None) -> Self:
        """ Clone directly from another element without re-encoding """
        assert not self._content_set, "Content already set"
        assert other._content_set, "Other content not set"

        self.name = name or other.name
        self._value = other._value
        self._encoding = other._encoding
        self._content_set = True
        self._type = other._type
        self._type_set = other._type_set
        self._raw_content = other._raw_content
        self._processed_value = other._processed_value
        self._content_type = other._content_type

        return self

    def _join_name(self, parts: typing.Iterable[str | PurePosixPath]) -> str:
        return '.'.join(str(part) for part in parts)

    def _create_content_from_node(self, node: CT, direct_parent: PCT, ref_parent: PCT | None, *,
                                  args: BundleFactoryArguments) -> Self:
        """ Set the attributes from the XML dom node

        Child content is saved as-is and processing is postponed until the value or type properties are accessed

        :param node: the node to copy the attributes from
        :param direct_parent: the node's direct parent
        :param ref_parent: the node's ref-parent, the predecessor to which the 'ref' attribute refers
        """
        assert not self._content_set and not self._type_set, "Content already set"

        name_parts = self._get_attr_base_parts('name', node, direct_parent, ref_parent)
        # src_parts = self._get_attr_base_parts(
        #     'src', node, direct_parent, ref_parent,
        #     lambda src: src[5:] if src.lower().startswith('file:') else src
        # )

        self._name = self._join_name(name_parts) if name_parts else None
        # self._src = PurePosixPath(*src_parts) if src_parts else None
        self._value = getattr(node, 'value', None)

        raw_content: typing.MutableSequence[RawType] = deque()
        for item in node.content:
            if isinstance(item, str):
                raw_content.append(item)
            else:
                if item.qname == true_qname:
                    raw_content.append(True)
                elif item.qname == false_qname:
                    raw_content.append(False)
                elif item.qname == none_qname:
                    raw_content.append(None)
                else:
                    msg = f"Unknown child element {item.qname}"
                    if args.validate_xml:
                        raise BundleFormatError(msg)
                    else:
                        warnings.warn(msg)

        self._raw_content = tuple(raw_content) if raw_content else None
        self._processed_value = None
        self._content_type = None

        self._content_set = True
        self._type_set = True
        return self

    def _process_value(self) -> tuple[PT, str | None]:
        """ Get the processed value and content_type by decoding `value` attribute or raw content.
        If there is no content raises :py:exc:`NoContent`

        Returns the processed value and the type
        """
        assert self._content_set, "No content provided"
        # assert self._src is None

        if self._processed_value is None:
            if self._value is not None:
                typename = self._type
                typename = ALTERNATE_VALUE_TYPES.get(typename, typename)

                if typename and typename not in VALUE_TYPE_MAP:
                    warnings.warn(f"Invalid type {typename!r} for option {self.name!r} ignored")

                datatype = VALUE_TYPE_MAP.get(typename, str)
                try:
                    self._processed_value = (datatype(self._value),)
                except ValueError:
                    self._processed_value = (self._value,)

                self._content_type = None

            elif self._raw_content is not None or self._encoding is not None:
                content: typing.MutableSequence[PT] = deque()
                content_text: str = ''
                if self._raw_content is not None:
                    has_text_content: bool = False
                    for item in self._raw_content:
                        if isinstance(item, str):
                            content_text += item
                            has_text_content |= bool(item.lstrip())

                        elif has_text_content:
                            warnings.warn("Mixed content of strings and elements not supported")

                        else:
                            content.append(item)
                else:
                    # Empty content is considered to be an empty string
                    has_text_content: bool = True

                if has_text_content:
                    if self._encoding:
                        decoded = decode_data(content_text, self._encoding)
                        self._processed_value = (decoded,)
                    else:
                        self._processed_value = (content_text,)
                else:
                    self._processed_value = (content[0],)

                self._content_type = self._type

            else:
                # No content at all
                self._processed_value = tuple()
                self._content_type = None

        return self._processed_value[0] if self._processed_value else NO_CONTENT, self._content_type

    def _create_raw_content(self, *, args: BundleConstructionArguments | None = None):
        """ Update __raw_content, __encoding, _type and _value attributes based on __processed_value and __content_type

        If `args.optimize` is set, this will re-encode existing content
        """
        # assert self._src is None
        assert self._content_set, "No content provided"

        optimize = args and args.optimize

        if self._processed_value is None and optimize:
            self._processed_value = self._process_value()
            self._raw_content = None
            self._value = None

        if self._processed_value is not None and self._raw_content is None and self._value is None:
            value = self._processed_value[0] if self._processed_value else None
            if not self._processed_value:
                # Empty tuple, indicates empty node
                self._raw_content = tuple()
                self._encoding = None
                self._value = None
                self._type = None
                if self._content_type:
                    warnings.warn('"type" attribute cannot be used for empty content nodes')

            elif value is None or isinstance(value, bool):
                # Encoded using child elements <none/>, <true/> or <false/>
                self._raw_content = (value,)
                self._encoding = None
                self._value = None
                self._type = None

                if self._content_type:
                    warnings.warn('"type" attribute cannot be combined with None or boolean values')

            elif self._content_type is not None or isinstance(value, bytes) or (
                    isinstance(value, str) and (len(value) > self.MAX_VALUE_LENGTH or not is_printable(value))
            ):
                if self.HAS_ENCODING:
                    # Text content that needs to be encoded as child content
                    encoded, encoding = encode_data(value)
                elif isinstance(value, bytes):
                    encoded, encoding = value.decode('utf-8'), None
                else:
                    encoded, encoding = value, None

                self._raw_content = (encoded,)
                self._encoding = encoding
                self._value = None
                self._type = self._content_type

            else:
                # Something that can be stored in the value attribute
                self._raw_content = None
                self._encoding = None
                self._value = str(value)
                self._type = None

                if isinstance(value, int):
                    self._type = 'integer'
                elif isinstance(value, (float, Decimal)):
                    self._type = 'float'
                elif not isinstance(value, (bytes, str)):
                    raise ValueError(f"Invalid type {type(value)} for attribute `value`")

                if self._content_type:
                    warnings.warn('"type" attribute cannot be used for numeric values')

    def __construct_raw_node(self, item: typing.Any) -> AnyElement | str:
        if isinstance(item, bool):
            return AnyElement(qname=true_qname if item else false_qname)
        elif item is None:
            return AnyElement(qname=none_qname)
        elif isinstance(item, str):
            return item

        raise ValueError("Unable to convert convert element {}".format(item))

    # noinspection PyProtectedMember
    def _construct_content(self, node: CT, *, args: BundleConstructionArguments) -> CT:
        """ Update the attributes of an XML dom node

        :param node: The node to update
        :return: node
        """
        self._create_raw_content(args=args)

        if self._name is not None:
            setattr(node, 'name', str(self._name))

        # if self._src is not None:
        #     setattr(node, 'src', str(self._src))

        if self._encoding is not None:
            setattr(node, 'encoding', self._encoding)

        if self._value is not None:
            setattr(node, 'value', self._value)

        if self._type is not None:
            setattr(node, 'type_value', self._type)

        if self._raw_content:
            node.content = [
                self.__construct_raw_node(item)
                for item in self._raw_content
            ]

        return node

    def has_inline_content(self) -> bool:
        """ Returns True if element has inline content, without processing the content
        """
        assert self._content_set, "No content provided"
        return (
            self._encoding is not None or self._value is not None
            or self._raw_content is not None or self._processed_value is not None
        )

    def has_inline_text_content(self) -> bool:
        """ Returns True if self.value would return text content
        (either bytes or str), without converting the content.
        """
        assert self._content_set, "No content provided"

        if self._encoding is not None or (
            self._processed_value and len(self._processed_value) == 1
                and isinstance(self._processed_value[0], (bytes, str))
        ):
            return True

        elif self._raw_content is not None:
            for item in self._raw_content:
                if isinstance(item, str):
                    if item.strip() != '':
                        return True
                else:
                    return False

        elif self._value is not None:
            return self._type is None or self._type == 'string'

        return False

    # noinspection PyMethodMayBeStatic
    def has_attachment_content(self) -> bool:
        """ Returns True if this element has an existing attachment  """
        return False

    def has_text_content(self) -> bool:
        """ Returns True if the element has text content """
        return self.has_inline_text_content() or self.has_attachment_content()

    def _get_bytes_content(self) -> bytes:
        if self.has_inline_text_content():
            value = self._process_value()[0]
            return value.encode('utf-8') if isinstance(value, str) else value

        raise ValueError


class ContentBasicElement(typing.Generic[CT, PCT], ContentElementBase[ContentBasicProcessedType, CT, PCT], ABC):
    """ A basic content element. Contents can be string or boolean values.
    """
    VALID_PROCESSED_TYPES: typing.ClassVar[tuple[type, ...]] = (str, bool)
    HAS_ENCODING: typing.ClassVar[bool] = False


class ContentFullElement(typing.Generic[CT, PCT], ContentElementBase[ContentFullProcessedType, CT, PCT], ABC):
    """ A full content element.

    Contents can be string, bytes, boolean, integer, float or :py:class:`decimal.Decimal` values.
    """
    VALID_PROCESSED_TYPES: typing.ClassVar[tuple[type, ...]] = (
            ContentBasicElement.VALID_PROCESSED_TYPES + (bytes, int, float, Decimal)
    )
    HAS_ENCODING: typing.ClassVar[bool] = True

    @property
    def type_(self) -> str | None:
        """ The `type` attribute. Indicates the type of the `value` attribute: string, integer or float """
        return self._process_value()[1]

    @type_.setter
    def type_(self, type_: str | None):
        super()._set_type(type_)

    @property
    def encoding(self) -> str | None:
        """ `encoding` attribute: read-only, the encoding is automatically determined from the value """
        self._create_raw_content()
        return self._encoding

    # noinspection PyShadowingBuiltins,PyMethodOverriding
    def _create_content(self, *,
                        name: str,
                        value: ContentBasicProcessedType = NO_CONTENT,
                        type_: str | None = None) -> Self:
        self.name = name
        self.value = value
        self.type_ = type_
        return self

    def _create_content_from_node(self, node: CT, direct_parent: PCT, ref_parent: PCT | None, *,
                                  args: BundleFactoryArguments) -> Self:
        """ Set the attributes from the XML dom node

        Child content is saved as-is and processing is postponed until the value or type properties are accessed

        :param node: the node to copy the attributes from
        :param direct_parent: the node's direct parent
        :param ref_parent: the node's ref-parent, the predecessor to which the 'ref' attribute refers
        """
        super()._create_content_from_node(node, direct_parent, ref_parent, args=args)

        self._type = getattr(node, 'type_value', None)
        self._encoding = getattr(node, 'encoding', None)

        return self


class ContentAttachmentElement(NamePathMixin, SrcAttachmentMixin, ContentFullElement[CT, PCT], ABC):
    """ A full content element supporting attachments.

    Contents can be string, bytes, boolean, integer, float or :py:class:`decimal.Decimal` values,
    or provided as an attachment using the `src` attribute.
    """
    @property
    def type_(self) -> str | None:
        """ The `type` attribute. """
        if self.has_attachment_content():
            return self._type
        else:
            return self._process_value()[1]

    @type_.setter
    def type_(self, type_: str | None):
        super()._set_type(type_)

    def _create_raw_content(self, *, args: BundleConstructionArguments | None = None):
        if self.has_attachment_content():
            self._type = self._content_type
            self._raw_content = None
            self._encoding = None
        else:
            return super()._create_raw_content(args=args)

    def _process_value(self) -> tuple[PT, str | None]:
        """ Get the processed value and content_type by decoding `value` attribute or raw content.

        :returns: the processed value and the type
        :raises NoContent: if there is no content (empty XML node)
        :raises AttachmentContent: if the content is in an attachment (`src` attribute set)
        """
        if self.has_attachment_content():
            raise AttachmentContent

        return super()._process_value()

    # noinspection PyShadowingBuiltins
    def _create_content(self, *,
                        name: str | PurePath | None = None,
                        src: AttachmentSrc | PurePath | None = None,
                        value: ContentBasicProcessedType = NO_CONTENT,
                        type_: str | None = None) -> Self:

        assert not self._content_set and not self._type_set, "Content already set"
        assert value is NO_CONTENT or src is None, "Cannot set both `value` and `src`"

        self.name = name
        self.src = src
        self.value = value
        self.type_ = type_

        return self

    def _clone_content(self, other: Self, *, name: str | None = None) -> Self:
        assert other.has_inline_content(), "Can only clone inline attachments"
        super()._clone_content(other, name=name)
        self.src = None
        return self

    def _create_content_from_node(self, node: CT, direct_parent: PCT, ref_parent: PCT | None, *,
                                  args: BundleFactoryArguments) -> Self:
        """ Set the attributes from the XML dom node

        Child content is saved as-is and processing is postponed until the value or type properties are accessed

        :param node: the node to copy the attributes from
        :param direct_parent: the node's direct parent
        :param ref_parent: the node's ref-parent, the predecessor to which the 'ref' attribute refers
        """
        super()._create_content_from_node(node, direct_parent, ref_parent, args=args)

        src_set = False
        if not self.has_inline_content():
            # Collect `src` path.
            parts = deque()

            value = node.src
            if value is None:
                value = node.name
            elif value.lower().startswith('file:'):
                value = value[5:]

            if value is not None:
                parent_value = getattr(direct_parent, 'basesrc', None)
                if parent_value is not None:
                    parts.append(parent_value)

                if ref_parent:
                    ref_value = getattr(ref_parent, 'basesrc', None)
                    if ref_value is not None:
                        parts.append(ref_value)

                parts.append(value)

            if parts:
                self.src = AttachmentSrc(PurePosixPath(*parts), self.bundle, validate=args.validate_signature)
                src_set = True

        if not src_set:
            self.src = None

        return self

    # noinspection PyProtectedMember,PyMethodOverriding
    def _construct_content(self, node: CT, basesrc: PurePosixPath, *, args: BundleConstructionArguments) -> CT:
        """ Update the attributes of an XML dom node

        :param node: The node to update
        :return: node
        """
        super()._construct_content(node, args=args)

        if self.has_attachment_content():
            export_src = self._export_path(basesrc / self.name)
            src_attr = str(export_src.relative_to(basesrc))
            if src_attr != str(self.name) or args.legacy:
                setattr(node, 'src', src_attr)

        return node

    # Override AttachmentMixin functions to add support for inline content

    def has_writable_content(self):
        return super().has_writable_content() or self.has_inline_text_content()

    def file_size(self, path: str | PurePosixPath | None = None) -> int | None:
        """ Get file size for the content.

        :return: The file size
        """
        if self.has_inline_text_content():
            if path is not None:
                raise FileNotFoundError(path)

            return len(self.value)

        return SrcAttachmentMixin.file_size(self, path)

    def is_dir(self, path: str | PurePosixPath | None = None) -> bool:
        return not self.has_inline_text_content() and SrcAttachmentMixin.is_dir(self, path)

    def open(self, path: str | PurePosixPath | None = None) -> typing.BinaryIO:
        if self.has_inline_text_content():
            if path:
                raise FileNotFoundError

            return BytesIO(self._get_bytes_content())

        return SrcAttachmentMixin.open(self, path)

    def read(self, path: str | PurePosixPath | None = None) -> bytes:
        if self.has_inline_text_content():
            if path:
                raise FileNotFoundError

            return self._get_bytes_content()

        return SrcAttachmentMixin.read(self, path)

    def _dest_name(self) -> PurePath | None:
        return self.name or SrcAttachmentMixin._dest_name(self)

    def _copy_file(self, dest_path: Path):
        if self.has_inline_text_content():
            with dest_path.open('wb') as writer:
                writer.write(self._get_bytes_content())
        else:
            SrcAttachmentMixin._copy_file(self, dest_path)


# Extend the docstrings with the generic documentation of Element
if Element.__doc__:
    if ContentBasicElement.__doc__:
        ContentBasicElement.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])

    if ContentFullElement.__doc__:
        ContentFullElement.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])

    if ContentAttachmentElement.__doc__:
        ContentAttachmentElement.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])
