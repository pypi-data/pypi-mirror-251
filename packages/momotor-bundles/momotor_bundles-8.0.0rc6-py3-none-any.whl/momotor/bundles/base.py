from __future__ import annotations

import abc
import contextlib
import dataclasses
import importlib.resources
import pathlib
import tempfile
import typing
import warnings
import zipfile
from abc import ABC
from io import BytesIO, open as io_open

from xsdata.exceptions import ParserError
from xsdata.utils.namespaces import build_qname

from momotor.bundles.binding.momotor_1_0 import __NAMESPACE__
from momotor.bundles.const import BundleFormat, BundleCategory
from momotor.bundles.elements.base import Element
from momotor.bundles.exception import BundleError, BundleLoadError, InvalidBundle, BundleFormatError
from momotor.bundles.mixins.attachments import SrcAttachmentMixin
from momotor.bundles.parsers.config import BundleParserConfig
from momotor.bundles.parsers.handlers.exceptions import ValidationError
from momotor.bundles.parsers.xml import XmlBundleParser
from momotor.bundles.serializers.config import BundleSerializerConfig
from momotor.bundles.serializers.xml import XmlBundleSerializer
from momotor.bundles.utils.arguments import BundleFactoryArguments, BundleConstructionArguments, \
    FileConstructionArguments, DirectoryConstructionArguments
from momotor.bundles.utils.detect import detect_bundle_type
from momotor.bundles.utils.lxml import use_lxml
from momotor.bundles.utils.zipwrapper import ZipWrapper

try:
    from typing import Self  # py3.11+
except ImportError:
    from typing_extensions import Self

__all__ = ["Bundle"]


SCHEMA_PACKAGE_LOCATION = 'momotor.bundles:schema/momotor-1.0.xsd'
SCHEMA_NAMESPACE_LOCATION = 'http://momotor.org/schema/momotor-1.0.xsd'


# noinspection PyTypeChecker
AT = typing.TypeVar('AT', bound=dataclasses.dataclass())
CT = typing.TypeVar('CT', bound=object)


def _merge_args(cls: type[AT], args: AT | None, kwargs: typing.Mapping) -> AT:
    """ Merge arguments dataclass with keyword arguments

    :param cls: type of the arguments dataclass
    :param args: the arguments
    :param kwargs: the keywords
    :return: dataclass with `args` updated with `kwargs`
    """
    if args is None:
        return cls(**kwargs)
    elif kwargs:
        return dataclasses.replace(args, **kwargs)

    return args


@contextlib.contextmanager
def validation_schema() -> contextlib.AbstractContextManager[pathlib.Path]:
    """ Extract validation schema files from the package and return a temporary path to momotor-1.0.xsd

    :return: path to the schema file
    """
    package_name, schema_location = SCHEMA_PACKAGE_LOCATION.split(':')
    if '/' in schema_location:
        schema_dir, schema_file_name = schema_location.rsplit('/', 1)
    else:
        schema_dir, schema_file_name = None, schema_location

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = pathlib.Path(temp_dir)

        schema_path = importlib.resources.files(package_name)
        if schema_dir:
            schema_path = schema_path.joinpath(schema_dir)

        for schema_file in schema_path.iterdir():
            assert schema_file.is_file(), 'nested directories in schema are not supported'
            with (temp_path / schema_file.name).open('wb') as dst_file:
                dst_file.write(schema_file.read_bytes())

        yield temp_path / schema_file_name


class Bundle(Element[CT], typing.Generic[CT], ABC):
    """ Access a Momotor bundle

    :param base: A path to the directory containing the XML source file in `instance`.
                 Any file path is relative to this base.
    :param zip_wrapper: A :py:class:`~momotor.bundles.utils.zipwrapper.ZipWrapper` instance for the zip-file
                        containing the bundle, for internal use by the :py:meth:`~Bundle.from_bytes_factory` and
                        :py:meth:`~Bundle.from_file_factory` methods
    """
    _base: pathlib.Path | None
    _zip_wrapper: ZipWrapper | None
    _attachments: set[SrcAttachmentMixin]
    _attachment_paths: set[pathlib.PurePosixPath]

    def __init__(self, base: str | pathlib.Path | None = None, zip_wrapper: ZipWrapper = None):
        Element.__init__(self, self)

        self._base = pathlib.Path(base) if base else None
        self._zip_wrapper = zip_wrapper
        self._attachments = set()
        self._attachment_paths = set()

    def recreate(self, target_bundle: "Bundle", **kwargs) -> typing.NoReturn:
        raise ValueError("Cannot recreate a bundle directly")

    def close(self):
        """ Close bundle and release all files and resources held.

        Any access to the bundle after calling :py:meth:`~momotor.bundles.Bundle.close` is undefined.
        """
        if self._zip_wrapper:
            self._zip_wrapper.close()

    @staticmethod
    @abc.abstractmethod
    def get_default_xml_name() -> str:
        """ Get the default XML file name
        """
        ...

    @classmethod
    def get_root_tag(cls) -> str:
        """ Get the XML root tag for this bundle
        """
        return cls.get_node_type().Meta.name

    @classmethod
    def get_root_qname(cls) -> str:
        """ Get the XML root tag for this bundle
        """
        return build_qname(cls.get_node_type().Meta.namespace, cls.get_root_tag())

    @staticmethod
    @abc.abstractmethod
    def get_category() -> BundleCategory:
        """ Get the category for this bundle
        """
        ...

    def _register_attachment(self, attachment: SrcAttachmentMixin):
        if attachment.src:
            self._attachments.add(attachment)

    def _has_attachments(self) -> bool:
        return bool(self._attachments)

    def _register_attachment_export_path(self, path: pathlib.PurePosixPath):
        if path in self._attachment_paths:
            raise FileExistsError

        self._attachment_paths.add(path)

    # Reading

    @classmethod
    def __get_parser(cls, args: BundleFactoryArguments, stack: contextlib.ExitStack) -> XmlBundleParser:
        validate_xml = args.validate_xml
        if validate_xml is None:
            validate_xml = True

        config = BundleParserConfig(
            fail_on_unknown_properties=validate_xml
        )

        if use_lxml(args.use_lxml):
            from .parsers.handlers.lxml import LxmlBundleEventHandler as EventHandler

            config.process_xinclude = True
            config.process_xslt = True
            if args.validate_xml is not False:  # also validate when args.validate_xml is None
                config.validation_schema_path = stack.enter_context(validation_schema())

        else:
            from .parsers.handlers.xml import XmlBundleEventHandler as EventHandler

            if args.validate_xml:  # only warn when args.validate_xml is explicitly True
                warnings.warn('XML validation is only supported when using lxml')

        return XmlBundleParser(
            config=config,
            handler=EventHandler,
            expected_root_qname=cls.get_root_qname()
        )

    @classmethod
    def _from_io(cls, io: typing.BinaryIO, stack: contextlib.ExitStack, *,
                 args: BundleFactoryArguments, **updated_args) -> tuple[CT, BundleFactoryArguments]:
        args = dataclasses.replace(args, **updated_args)
        parser = cls.__get_parser(args, stack)

        try:
            return parser.parse(io, cls.get_node_type()), args

        except BundleError:
            raise

        except (ParserError, ValidationError) as e:
            raise BundleFormatError(str(e))

        except Exception as e:
            raise BundleLoadError(str(e))

    @classmethod
    def from_file_factory(cls, path: str | pathlib.Path, *,
                          args: BundleFactoryArguments | None = None, **kwargs) -> Self:
        """Read bundle from a local file or directory.
        When using the :py:class:`~momotor.bundles.Bundle` base class, uses :py:meth:`detect` to autodetect
        the type of bundle. When using a specific bundle class, will raise an
        :py:exc:`~momotor.bundles.exception.InvalidBundle` exception if the file is the wrong bundle type.

        Make sure to call :py:meth:`~momotor.bundles.Bundle.close` either explicitly or using
        :py:func:`contextlib.closing` when done with the bundle to release all resources

        :param path: Either a file or directory.
                     When it is a file, it can be an XML file or a zip file.
                     When it is a directory, that directory should contain a <bundle>.xml file
        :param args: arguments for the factory
        :param kwargs: alternative way to provide the arguments. Arguments in kwargs override arguments in args
        :return: the bundle
        :raises: :py:exc:`~momotor.bundles.exception.InvalidBundle` if path does not contain a valid bundle
        """
        with contextlib.ExitStack() as stack:
            args = _merge_args(BundleFactoryArguments, args, kwargs)

            if cls is Bundle:
                return detect_bundle_type(path, args).from_file_factory(path, args=args)

            path = pathlib.Path(path)
            xml_type = cls.get_root_tag()
            xml_name = args.xml_name
            if not xml_name:
                xml_name = cls.get_default_xml_name()

            if zipfile.is_zipfile(path):
                base = None
                zip_wrapper = ZipWrapper(path=path)
                try:
                    zip_file = stack.enter_context(zip_wrapper)
                    zip_io = stack.enter_context(zip_file.open(xml_name))

                    root, args = cls._from_io(
                        zip_io, stack,
                        args=args,
                        xml_name=xml_name,
                        location_base=f"{args.location_base or path}:{xml_name}"
                    )

                except KeyError:
                    raise InvalidBundle("A {} bundle should contain a {} file in the root".format(xml_type, xml_name))

            else:
                zip_wrapper = None
                if path.is_dir():
                    base, path = path, path / xml_name
                    if not path.exists():
                        raise InvalidBundle("A {} bundle should contain a {} file in the root".format(xml_type, xml_name))
                else:
                    base = path.parent

                io_ = stack.enter_context(path.open('rb'))
                root, args = cls._from_io(
                    io_, stack,
                    args=args,
                    xml_name=xml_name,
                    location_base=str(args.location_base or path)
                )

            # noinspection PyProtectedMember
            return cls(base, zip_wrapper)._create_from_node(root, args=args)

    @classmethod
    def from_bytes_factory(cls, data: bytes | memoryview, *,
                           args: BundleFactoryArguments | None = None, **kwargs) -> Self:
        """Read bundle from memory, either a :py:class:`bytes` or :py:class:`memoryview` object.
        When using the :py:class:`~momotor.bundles.Bundle` base class, uses :py:meth:`detect` to autodetect
        the type of bundle. When using a specific bundle class, will raise an
        :py:exc:`~momotor.bundles.exception.InvalidBundle` exception if the file is the wrong bundle type.

        Make sure to call :py:meth:`~momotor.bundles.Bundle.close` either explicitly or using
        :py:func:`contextlib.closing` when done with the bundle to release all resources

        :param data: Bundle data
        :param args: arguments for the factory
        :param kwargs: alternative way to provide the arguments. Arguments in kwargs override arguments in args
        :return: the bundle
        :raises: :py:exc:`~momotor.bundles.exception.InvalidBundle` if data does not contain a valid bundle
        """
        with contextlib.ExitStack() as stack:
            args = _merge_args(BundleFactoryArguments, args, kwargs)

            if cls is Bundle:
                return detect_bundle_type(data, args).from_bytes_factory(data, args=args)

            xml_type = cls.get_root_tag()
            xml_name = args.xml_name
            if not xml_name:
                xml_name = cls.get_default_xml_name()

            data_io = BytesIO(data)
            if zipfile.is_zipfile(data_io):
                zip_wrapper = ZipWrapper(content=data)
                try:
                    zip_file = stack.enter_context(zip_wrapper)
                    xml_io = stack.enter_context(zip_file.open(xml_name))
                    root, args = cls._from_io(
                        xml_io, stack,
                        args=args,
                        xml_name=xml_name,
                        location_base=f"{args.location_base or '<zip file>'}/{xml_name}"
                    )

                except KeyError:
                    raise InvalidBundle("A {} bundle should contain a {} file in the root".format(xml_type, xml_name))

            else:
                zip_wrapper = None
                data_io.seek(0)
                root, args = cls._from_io(
                    data_io, stack,
                    args=args,
                    xml_name=xml_name,
                    location_base=str(args.location_base) if args.location_base else None
                )

            # noinspection PyProtectedMember
            return cls(None, zip_wrapper)._create_from_node(root, args=args)

    # Writing

    # noinspection PyMethodMayBeStatic
    def __get_serializer(self, *, args: BundleConstructionArguments) -> XmlBundleSerializer:
        if use_lxml(args.use_lxml):
            from .serializers.writers.lxml import LxmlBundleEventWriter as EventWriter
        else:
            from .serializers.writers.xml import XmlBundleEventWriter as EventWriter

        config = BundleSerializerConfig(
            pretty_print=args.pretty_xml,
            encoding=args.encoding,
        )

        return XmlBundleSerializer(
            config=config,
            writer=EventWriter,
        )

    def _to_xml(self, args: BundleConstructionArguments) -> bytes:
        """ Export the bundle to an XML document

        :param args: arguments for the construction
        :return: utf-8 encoded XML document
        """
        return self.__get_serializer(
            args=args
        ).render(
            self._construct_node(args=args),
            ns_map={
                None: __NAMESPACE__
            }
        ).encode(args.encoding)

    # noinspection PyShadowingBuiltins
    def to_buffer(self, buffer: typing.BinaryIO, *,
                  args: FileConstructionArguments | None = None, **kwargs) -> BundleFormat:
        """ Export the bundle to a :py:class:`~typing.BinaryIO` buffer and close it.

        If the `zip` option is False and the bundle does not contain any attachments, will generate a plain
        XML bundle, otherwise it will generate a zip compressed bundle with the bundle XML file located in the
        root of the zip file.

        Any access to the bundle after calling :py:meth:`~momotor.bundles.Bundle.to_buffer` is undefined.

        :param buffer: buffer to export into
        :param args: arguments for the construction
        :param kwargs: alternative way to provide the arguments. Arguments in kwargs override arguments in args
        :return: created format, either :py:class:`~momotor.bundles.const.BundleFormat`\ ``.XML``
            or :py:class:`~momotor.bundles.const.BundleFormat`\ ``.ZIP``
        """
        args = _merge_args(FileConstructionArguments, args, kwargs)

        with contextlib.closing(self):
            if not self._has_attachments() and not args.zip:
                buffer.write(self._to_xml(args))
                return BundleFormat.XML

            compression_args = {
                'compression': args.compression,
                'compresslevel': args.compresslevel
            }

            with zipfile.ZipFile(buffer, mode='w', **compression_args) as zip_file:
                xml_name = args.xml_name
                if not xml_name:
                    xml_name = self.get_default_xml_name()

                zip_file.writestr(xml_name, self._to_xml(args))

                for attachment in self._attachments:
                    attachment._export_to_zip(zip_file, args)

            return BundleFormat.ZIP

    # noinspection PyShadowingBuiltins
    def to_file(self, fd_or_path: int | str | pathlib.Path, *,
                args: FileConstructionArguments | None = None, **kwargs) -> BundleFormat:
        """
        Export the bundle to a file and close it.

        If the `zip` option is False and the bundle does not contain any attachments, will generate a plain
        XML bundle, otherwise it will generate a zip compressed bundle with the bundle XML file located in the
        root of the zip file.

        Any access to the bundle after calling :py:meth:`~momotor.bundles.Bundle.to_file` is undefined.

        :param fd_or_path: either an open file descriptor, or a path. The file descriptor will be closed
        :param args: arguments for the construction
        :param kwargs: alternative way to provide the arguments. Arguments in kwargs override arguments in args
        :return: created format, either :py:class:`~momotor.bundles.const.BundleFormat`\ ``.XML``
            or :py:class:`~momotor.bundles.const.BundleFormat`\ ``.ZIP``
        """

        if isinstance(fd_or_path, int):
            opener = io_open(fd_or_path, 'w+b')
        else:
            opener = pathlib.Path(fd_or_path).open('w+b')

        with opener as f:
            return self.to_buffer(f, args=args, **kwargs)

    def to_directory(self, path: pathlib.Path, *, args: DirectoryConstructionArguments | None = None, **kwargs) -> None:
        """
        Export the bundle to a directory.

        Writes the XML file to the given `path` and all the bundle's attachments in the
        right location relative to the XML file.

        Any access to the bundle after calling :py:meth:`~momotor.bundles.Bundle.to_directory` is undefined.

        :param path: path of the directory. Will be created if it does not exist
        :param args: arguments for the construction
        :param kwargs: alternative way to provide the arguments. Arguments in kwargs override arguments in args
        """
        args = _merge_args(DirectoryConstructionArguments, args, kwargs)

        if not path.exists():
            path.mkdir(mode=args.dir_mode, parents=True)

        with contextlib.closing(self):
            xml_name = args.xml_name
            if not xml_name:
                xml_name = self.get_default_xml_name()

            # Write XML file
            (path / xml_name).write_bytes(
                self._to_xml(args)
            )

            # Export any attachments
            for attachment in self._attachments:
                # noinspection PyProtectedMember
                attachment._export_to_dir(path)

    @classmethod
    def detect(cls, path_or_data: pathlib.Path | bytes | memoryview,
               *, args: BundleFactoryArguments | None = None, **kwargs) -> type["Bundle"]:
        """ Detect type of bundle and return the corresponding class.

        :param path_or_data: A :py:class:`~pathlib.Path` to the bundle file or directory, or a :py:class:`bytes` or
                :py:class:`memoryview` containing a bundle XML or ZIP file
        :param args: arguments for the detection
        :param kwargs: alternative way to provide the arguments. Arguments in kwargs override arguments in args
        :return: The matching :py:class:`~momotor.bundles.Bundle` class, either
                :py:class:`~momotor.bundles.RecipeBundle`,
                :py:class:`~momotor.bundles.ConfigBundle`,
                :py:class:`~momotor.bundles.ProductBundle`,
                :py:class:`~momotor.bundles.ResultsBundle`, or
                :py:class:`~momotor.bundles.TestResultBundle`
        :raises: :py:exc:`FileNotFoundError` if path does exist
        :raises: :py:exc:`~momotor.bundles.exception.InvalidBundle` if path does not contain a bundle
        """
        if cls is not Bundle:
            raise TypeError('detect() must be called from the `Bundle` base class')

        args = _merge_args(BundleFactoryArguments, args, kwargs)
        return detect_bundle_type(path_or_data, args)
