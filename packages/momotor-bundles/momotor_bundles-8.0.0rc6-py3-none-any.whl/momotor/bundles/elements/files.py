from __future__ import annotations

import typing
import warnings
from pathlib import PurePosixPath, Path, PurePath

import momotor.bundles
from momotor.bundles.binding import FileComplexType, FilesComplexType
from momotor.bundles.elements.base import Element
from momotor.bundles.elements.content import ContentAttachmentElement, NO_CONTENT, ContentBasicProcessedType
from momotor.bundles.elements.refs import resolve_ref
from momotor.bundles.elements.wildcard import WildcardAttrsMixin
from momotor.bundles.exception import BundleHashError
from momotor.bundles.mixins.attachments import SrcAttachmentsMixin, AttachmentSrc
from momotor.bundles.typing.element import ElementMixinProtocol
from momotor.bundles.utils.arguments import BundleConstructionArguments, BundleFactoryArguments
from momotor.bundles.utils.assertion import assert_elements_instanceof
from momotor.bundles.utils.boolean import to_bool
from momotor.bundles.utils.filters import FilterableTuple
from momotor.bundles.utils.nodes import get_nested_complex_nodes

try:
    from typing import TypeAlias  # py3.10+
except ImportError:
    from typing_extensions import TypeAlias

try:
    from typing import Self  # py3.11+
except ImportError:
    from typing_extensions import Self

__all__ = ['File', 'FilesMixin', 'FilesType']


class FileIntegrityError(Exception):
    pass


# def merge(ls: typing.Iterable = None, extra=None) -> list:
#     """ Filter all None values from `ls`, append `extra` """
#     ls = [item for item in ls if item is not None] if ls else []
#     if extra is not None:
#         ls.append(extra)
#     return ls


class File(
    ContentAttachmentElement[FileComplexType, FilesComplexType],
    WildcardAttrsMixin[FileComplexType]
):
    """ A File element encapsulating :py:class:`~momotor.bundles.binding.momotor_1_0.FileComplexType`
    """
    __unset: typing.ClassVar = object()
    _class: str | None = __unset
    _executable: bool = __unset

    @typing.final
    @property
    def class_(self) -> str | None:
        """ `class` attribute """
        assert self._class is not self.__unset, "Uninitialized attribute `class_`"
        return self._class

    @class_.setter
    def class_(self, class_: str | None):
        assert self._class is self.__unset, "Immutable attribute `class_`"
        assert class_ is None or isinstance(class_, str), "Invalid type for attribute `class_`"
        self._class = class_

    @typing.final
    @property
    def executable(self) -> bool:
        assert self._executable is not self.__unset, "Uninitialized attribute `executable`"
        return self._executable

    @executable.setter
    def executable(self, executable: bool):
        assert self._executable is self.__unset, "Immutable attribute `executable`"
        assert executable is True or executable is False
        self._executable = executable

    @staticmethod
    def get_node_type() -> type[FileComplexType]:
        return FileComplexType

    @staticmethod
    def _get_parent_type() -> type[FilesComplexType]:
        return FilesComplexType

    # noinspection PyShadowingBuiltins
    def create(self, *,
               class_: str | None = None,
               name: str | PurePosixPath | None = None,
               src: AttachmentSrc | PurePath | None = None,
               content: ContentBasicProcessedType = NO_CONTENT,
               type_: str | None = None,
               executable: bool = False,
               attrs: dict | None = None) -> Self:
        """ Set this file node's attributes.

        This creates an attachment for the bundle. The `src` or `content` parameters provide the content for the
        attachment. Only one of them can be set.
        When a file path is provided using `src`, the file must exist when the bundle is exported using one
        of the ``Bundle.to_*`` methods.

        Note that the `src` parameter of this method is not directly related to the `src` attribute of the `<file>`
        node in the generated XML when exporting the bundle, and how the `src` attribute is generated is an
        implementation detail of this library that can change between versions.
        Do not rely on an attachment being exported to a specific location in a generated zip bundle.

        :param class_: The `class` attribute of the file node
        :param name: The `name` attribute of the file node
        :param src: The source of the file. See note above.
        :param content: The content of the file. Defaults to :py:obj:`~momotor.bundles.elements.content.NO_CONTENT`.
        :param type_: The `type` attribute of the file node
        :param executable: The `executable` attribute of the file node
        :param attrs: Additional attributes of the file node
        """

        self._create_content(name=name, src=src, value=content, type_=type_)
        self.class_ = class_
        self.executable = bool(executable)
        self.attrs = attrs
        return self

    def _clone(self, other: Self, class_: str | None, name: str | PurePosixPath | None) -> Self:
        self._clone_content(other, name=name)
        self.class_ = class_ or other.class_
        self.executable = bool(other.executable)
        self.attrs = other.attrs
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", *,
                 class_: str | None = None, name: str | PurePosixPath | None = None) -> Self:
        """ Recreate this File in a target bundle, optionally changing the `class_` or `name`.

        If the node has a `src` attachment, the target bundle will *link* to the same file, the file will not be
        copied.

        :param target_bundle: The target bundle
        :param class_: New class for the file
        :param name: New name for the file
        :return:
        """
        file = File(target_bundle)

        if self.has_inline_content():
            return file._clone(self, class_, name)
        else:
            return file.create(
                class_=class_ or self.class_,
                name=name or self.name,
                src=self._src,
                type_=self.type_,
                executable=self.executable,
                attrs=self.attrs
            )

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: FileComplexType,
                          direct_parent: FilesComplexType,
                          ref_parent: FilesComplexType | None, *,
                          args: BundleFactoryArguments) -> Self:
        self._check_node_type(node)
        self._check_parent_type(direct_parent)
        self._check_parent_type(ref_parent, True)

        self._create_content_from_node(node, direct_parent, ref_parent, args=args)

        attrs = {**node.any_attributes}

        if 'executable' in attrs:
            executable_attr = attrs.pop('executable')
            if not isinstance(executable_attr, bool):
                if not args.legacy:
                    warnings.warn(f"boolean value for attribute 'executable' expected, got {type(executable_attr)} {executable_attr!r}")

                try:
                    executable = to_bool(executable_attr)
                except ValueError:
                    warnings.warn(f"invalid value {executable_attr!r} for attribute 'executable' ignored")
                    executable = False
            else:
                executable = executable_attr
        else:
            executable = False

        self.executable = executable
        self.attrs = attrs

        class_parts = self._get_attr_base_parts('class_value', node, direct_parent, ref_parent, base_attr='baseclass',
                                                allow_base_only=True)
        self.class_ = '.'.join(class_parts) if class_parts else None

        if args.validate_signature:
            import hashlib

            hash_values = {
                hash_name: hash_value
                for hash_name, hash_value in attrs.items()
                if hash_name in hashlib.algorithms_available
            }

            if hash_values and not self.validate_hashes(hash_values):
                raise BundleHashError(f"File hash mismatch (name={self.name!s} src={self.src!s} class={self.class_})")

        return self

    def _construct_node(self, basesrc: PurePosixPath, *, args: BundleConstructionArguments) -> FileComplexType:
        attrs = {}

        if self.has_attachment_content():
            if not self.is_dir():
                attrs['size'] = self.file_size()

                if args.sign_files:
                    hashes = self.file_hashes(args.hashers)

                    # Validate that the new hashes match the original ones if we know any
                    for hash_key, hash_value in hashes.items():
                        original_hash = self.attrs.get(hash_key)
                        if original_hash and hash_value != original_hash:
                            raise FileIntegrityError(f"File failed hash verification for f{hash_key}")

                    attrs.update(hashes)

                if self.executable:
                    attrs['executable'] = True

        # Except for the 'executable' attribute which is handled above, no other imported attributes (from self.attrs)
        # should be added to the newly constructed node
        return (
            self._construct_attrs(
                self._construct_content(
                    FileComplexType(
                        class_value=self.class_,
                        any_attributes=attrs
                    ),
                    basesrc,
                    args=args
                ),
                args=args
            )
        )

    def _join_name(self, parts: typing.Iterable):
        return PurePosixPath(*parts)

    def copy_to(self, destination: Path, *,
                name: PurePath | str | None = None,
                executable_attribute: bool = False) -> PurePath:

        dest_path = super().copy_to(destination, name=name)

        if executable_attribute and self.executable:
            # Set executable bits
            import stat
            dest_path.chmod(dest_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        return dest_path


if File.__doc__ and Element.__doc__:
    File.__doc__ += "\n".join(Element.__doc__.split("\n")[1:])


FilesType: TypeAlias = FilterableTuple[File]


# noinspection PyProtectedMember
class FilesMixin(SrcAttachmentsMixin[File]):
    """ Mixin for `Element` to add file support.
    """
    __unset: typing.ClassVar = object()
    _files: FilesType = __unset

    @typing.final
    @property
    def files(self) -> FilesType:
        """ `files` children """
        assert self._files is not self.__unset, "Uninitialized attribute `files`"
        return self._files

    @files.setter
    def files(self: ElementMixinProtocol | Self, files: typing.Iterable[File] | None):
        assert self._files is self.__unset, "Immutable attribute `files`"
        if files:
            self._files = assert_elements_instanceof(FilterableTuple(files), File, self.bundle)
        else:
            self._files = FilesType()

    def copy_files_to(self, destination: Path, *, files: typing.Sequence[File] | None = None) -> None:
        """ Copy files to a directory

        :param destination: destination for the files
        :param files: optionally a filtered list of files to copy
        """
        super()._copy_to(files or self.files, destination)

    def _collect_files(self: ElementMixinProtocol, parent: object,
                       ref_parents: typing.Iterable[typing.Iterable[FilesComplexType]], *,
                       args: BundleFactoryArguments) \
            -> typing.Generator[File, None, None]:

        files_node: FilesComplexType | None = None
        for tag_name, node in get_nested_complex_nodes(parent, 'files', 'file'):
            if tag_name == 'files':
                files_node = typing.cast(FilesComplexType, node)
            else:
                file_node = typing.cast(FileComplexType, node)
                if ref_parents:
                    ref_parent, node = resolve_ref('file', file_node, ref_parents)
                else:
                    ref_parent = None

                yield File(self.bundle)._create_from_node(node, files_node, ref_parent, args=args)

    # noinspection PyMethodMayBeStatic
    def _construct_files_nodes(self, basesrc: PurePosixPath = PurePosixPath('files'), *,
                               args: BundleConstructionArguments) \
            -> typing.Generator[FilesComplexType, None, None]:
        # TODO group by class
        # TODO basesrc is not needed when all files use inline content
        files = self.files
        if files:
            yield FilesComplexType(
                basesrc=str(basesrc),
                file=[
                    file._construct_node(basesrc, args=args)
                    for file in files
                ]
            )
