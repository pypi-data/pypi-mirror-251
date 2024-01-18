from __future__ import annotations

from dataclasses import dataclass

import pathvalidate
import shutil
import time
import typing
import warnings
import zipfile
from pathlib import Path, PurePath, PurePosixPath

import momotor.bundles
from momotor.bundles.typing.element import ElementMixinProtocol
from momotor.bundles.utils.arguments import FileConstructionArguments
from momotor.bundles.utils.zipwrapper import ZipWrapper

try:
    from typing import Self  # py3.11+
except ImportError:
    from typing_extensions import Self

CT = typing.TypeVar('CT')


class ZippedAttachment(FileNotFoundError):
    pass


def safe_path_name(name: str) -> str:
    """ Make a path name safe for use in ZIP files by converting it to pure ASCII

    Splits the string into parts separated by a period, then removes any character thats unsafe for use in a zip
    file name. If that changes the name, it adds a short hashcode to the part

    :param name:
    :return:
    """
    def safe_path_part(part: str) -> str:
        new_part = part.encode('ascii', 'replace').decode().replace('?', '')

        if part != new_part:
            import hashlib
            sig = hashlib.md5(part.encode('utf-8')).hexdigest()
            return f'{new_part}-{sig[:6]}'

        return new_part

    return '.'.join(safe_path_part(part) for part in name.split('.'))


@dataclass(frozen=True, init=False)
class AttachmentSrc:
    path: PurePath | None = None
    bundle: typing.Optional["momotor.bundles.Bundle"] = None

    def __init__(self,
                 path: PurePath | None = None,
                 bundle: typing.Optional["momotor.bundles.Bundle"] = None, *, validate=True):
        if path is None or path.is_absolute():
            # Ignore bundle if there is no path or it's absolute
            bundle = None
        elif hasattr(path, 'as_posix'):
            # Convert `path` to a `PurePosixPath` if possible
            path = PurePosixPath(path.as_posix())

        try:
            self.__validate(path, bundle)
        except FileNotFoundError as e:
            if validate:
                raise

            warnings.warn(str(e))
            path = None

        object.__setattr__(self, 'path', path)
        object.__setattr__(self, 'bundle', bundle)

    # noinspection PyProtectedMember
    @staticmethod
    def __validate(path: PurePath | None, bundle: typing.Optional["momotor.bundles.Bundle"]):
        if path is None:
            pass

        elif path.is_absolute():
            if not typing.cast(Path, path).exists():
                raise FileNotFoundError(f"attachment file or directory '{path!s}' does not exist")

        elif bundle is None:
            raise FileNotFoundError(f"attachment file or directory '{path!s}' is relative but no bundle is provided")

        elif bundle._base:
            if not (bundle._base / path).exists():
                raise FileNotFoundError(f"attachment file or directory '{path!s}' does not exist in related bundle {bundle}")

        elif bundle._zip_wrapper:
            with bundle._zip_wrapper as zip_file:
                name_list = zip_file.namelist()
                zip_path = str(path)
                zip_path_dir = zip_path + '/'
                for name in name_list:
                    if name == zip_path or name.startswith(zip_path_dir):
                        return

                raise FileNotFoundError(
                    f"attachment file or directory '{path!s}' does not exist in related zip bundle {bundle}. "
                )

        else:
            raise FileNotFoundError(f"attachment file or directory {path!r} does not exist in related bundle {bundle}")


class SrcAttachmentMixin:
    """ Mixin to provide attributes to refer to external files using the `src` attribute

    See :ref:`attachments` for how attachments are handled differently depending on whether the bundle
    is new or an existing one.
    """
    # TODO: use zipfile.Path once we no longer support Python 3.7

    _src: AttachmentSrc | None = None  # The current location of the attachment
    _export_src: PurePosixPath | None = None  # The location in the export bundle, converted to be safe
    _orig_src: PurePosixPath | None = None  # The original export path before making it safe

    @property
    def src(self) -> PurePath | None:
        """ `src` attribute: file path of the content.

        An absolute path (Path object) when referencing a standalone file, or a relative path (PurePosixPath object)
        when referencing a file in a bundle
        """
        assert self._src, '`src` not set'
        return self._src.path

    @property
    def src_bundle(self) -> typing.Optional["momotor.bundles.Bundle"]:
        """ The bundle `src` references to if it's a relative path
        """
        assert self._src, '`src` not set'
        return self._src.bundle

    # noinspection PyProtectedMember
    def __zip_wrapper(self) -> ZipWrapper:
        return self.src_bundle._zip_wrapper

    def has_bundle(self) -> bool:
        return self.src_bundle is not None

    def has_zip_bundle(self) -> bool:
        return self.has_bundle() and self.__zip_wrapper() is not None

    @src.setter
    def src(self: ElementMixinProtocol | Self, src: PurePath | AttachmentSrc | None):
        assert not self._src, "Immutable attribute `src`"
        assert src is None or isinstance(src, (PurePath, AttachmentSrc,))

        if not isinstance(src, AttachmentSrc):
            src = AttachmentSrc(src, self.bundle)

        self._src = src

        # noinspection PyProtectedMember
        self.bundle._register_attachment(self)

    @property
    def export_src(self) -> PurePosixPath | None:
        assert self._export_src is not None, '`export_src` not set'
        return self._export_src

    def has_attachment_content(self) -> bool:
        assert self._src, '`src` not set'
        return self._src.path is not None

    def has_writable_content(self) -> bool:
        return self.has_attachment_content()

    # noinspection PyProtectedMember
    @property
    def absolute_path(self: ElementMixinProtocol | Self) -> Path:
        path = self.src
        if path is None:
            raise FileNotFoundError(path)

        bundle = self.src_bundle
        if bundle:
            if bundle._zip_wrapper:
                raise ZippedAttachment

            if not bundle._base:
                raise FileNotFoundError(bundle._base)

            path = bundle._base / path

        return path.resolve(strict=True)

    def __get_fs_path(self, path: str | PurePosixPath | None) -> Path:
        src = self.absolute_path
        if path:
            src = src / path
        return src

    def __get_zip_path(self, path: str | PurePosixPath | None) -> str:
        src = self.src
        if path:
            src = src / path
        return str(src)

    def is_dir(self: ElementMixinProtocol | Self, path: str | PurePosixPath | None = None) -> bool:
        if not self.has_attachment_content() or (path and not self.is_dir(None)):
            raise FileNotFoundError(path)

        if self.has_zip_bundle():
            with self.__zip_wrapper() as zip_file:
                expected_path = self.__get_zip_path(path) + '/'

                try:
                    zip_file.getinfo(expected_path)
                except KeyError:
                    pass
                else:
                    return True

                name_list = zip_file.namelist()
                for name in name_list:
                    if name.startswith(expected_path):
                        return True

                return False

        return self.__get_fs_path(path).is_dir()

    @typing.overload
    def iterdir(self: ElementMixinProtocol | Self, *, include_empty_root: bool = False) \
            -> typing.Generator[PurePosixPath, None, None]:
        ...

    @typing.overload
    def iterdir(self: ElementMixinProtocol | Self, *, include_empty_root: bool = True) \
            -> typing.Generator[PurePosixPath | None, None, None]:
        ...

    def iterdir(self: ElementMixinProtocol | Self, *, include_empty_root: bool = False) \
            -> typing.Generator[PurePosixPath | None, None, None]:
        """ Recursively iterate the contents of a directory attachment.
        The returned paths are relative to `self.absolute_path`

        If the attachment is an empty directory and `include_empty_root` is True, a single None value is yielded
        """
        if not self.has_attachment_content() and self.is_dir():
            raise FileNotFoundError

        empty = True
        if self.has_zip_bundle():
            src = self.src

            with self.__zip_wrapper() as zip_file:
                for child in zip_file.namelist():
                    try:
                        path = PurePosixPath(child).relative_to(src)
                    except ValueError:
                        pass
                    else:
                        if str(path) != '.':
                            empty = False
                            yield path

        else:
            src = self.absolute_path

            def _walk_dir(path: Path):
                for dir_child in path.iterdir():
                    yield dir_child
                    if dir_child.is_dir():
                        yield from _walk_dir(dir_child)

            for child in _walk_dir(src):
                rel_child = child.relative_to(src)
                if hasattr(rel_child, 'as_posix'):
                    rel_child = rel_child.as_posix()

                empty = False
                yield rel_child

        if empty and include_empty_root:
            yield None

    def __validate_path(self, path: str | PurePosixPath | None):
        assert path is None or isinstance(path, (str, PurePosixPath))

        if not self.has_attachment_content():
            raise FileNotFoundError(path)

        if self.is_dir():
            if path is None:
                raise IsADirectoryError(path)

            if self.has_zip_bundle():
                with self.__zip_wrapper() as zip_file:
                    try:
                        info = zip_file.getinfo(self.__get_zip_path(path))
                    except KeyError:
                        raise FileNotFoundError(path)

                    if info.is_dir():
                        raise IsADirectoryError(path)

            else:
                fpath = self.__get_fs_path(path)
                if fpath.is_dir():
                    raise IsADirectoryError(path)
                elif not fpath.exists():
                    raise FileNotFoundError(path)

        elif path is not None:
            raise FileNotFoundError(path)

    def open(self: ElementMixinProtocol | Self, path: str | PurePosixPath | None = None) -> typing.BinaryIO:
        """ Open the attachment file for reading. Handles opening files directly from filesystem
        and from zipped bundles

        :param path: for directory attachments, `path` selects a file in that directory
        :return: the opened file
        :raises FileNotFoundError: if the element has no attachment (when `src` is None), or when it's a directory
            and `path` does not exist in that directory
        :raises IsADirectoryError: when it's a directory
        """
        self.__validate_path(path)

        if self.has_zip_bundle():
            with self.__zip_wrapper() as zip_file:
                return zip_file.open(self.__get_zip_path(path), 'r')
        else:
            return self.__get_fs_path(path).open('rb')

    def read(self, path: str | PurePosixPath | None = None) -> bytes:
        """ Read the contents of the attachment

        :param path: for directory attachments, `path` selects a file in that directory
        :return: A bytes object with the full file contents
        """
        with self.open(path) as f:
            return f.read()

    # Copying attachment into local filesystem

    def _dest_name(self) -> PurePath | None:
        if not self.is_dir() and self.src:
            return PurePath(self.src.name)

        return None

    def copy_to(self, destination: Path, *, name: PurePath | None = None) -> Path:
        """ Copy attachment to given directory

        If attachment is a file, creates a new file in the given directory. If `name` is provided this will be
        the name of the new file, otherwise the name of the source file is used.

        If attachment is a directory, copies the contents of the source directory to the destination directory.
        If `name` is provided it is created as a new directory inside the destination directory.

        Will not overwrite an existing file or directory.

        :param destination: base destination directory
        :param name: name
        :raises ValueError: when the attachment is not writeable as a file
        :raises FileExistsError: when a file already exists
        """
        if not self.has_writable_content():
            raise ValueError('Non-writable content')

        if not name:
            name = self._dest_name()

        dest_path = destination / name if name else destination
        if dest_path.exists():
            raise FileExistsError(dest_path)

        if self.is_dir():
            self._copy_dir(dest_path)
        else:
            self._copy_file(dest_path)

        return dest_path

    def _export_to_dir(self, destination: Path):
        """ Exports attachment to a new destination

        :param destination: base destination directory
        :raises FileExistsError: when a file already exists
        """
        if self.has_writable_content():
            export_dest = destination / self.export_src
            if self.is_dir():
                self._copy_dir(export_dest)
            else:
                self._copy_file(export_dest)

    def __copy_file_obj(self, name: PurePosixPath | None, dest_path: Path):
        if self.is_dir(name):
            dest_path.mkdir(exist_ok=True, parents=True)
        else:
            dest_path.parent.mkdir(exist_ok=True, parents=True)
            with self.open(name) as reader, dest_path.open('wb') as writer:
                shutil.copyfileobj(reader, writer)

    def _copy_file(self: ElementMixinProtocol | Self, dest_path: Path):
        self.__copy_file_obj(None, dest_path)

    def _copy_dir(self: ElementMixinProtocol | Self, dest_path: Path):
        for name in self.iterdir(include_empty_root=True):
            self.__copy_file_obj(name, dest_path / name if name else dest_path)

    def _export_to_zip(self, dst_zip_file: zipfile.ZipFile, args: FileConstructionArguments):
        """ Exports attachment to a zip file

        :raises ValueError: when the attachment is not writeable as a file
        :raises FileExistsError: when a file already exists
        """
        if self.has_writable_content():
            if self.is_dir():
                self._copy_dir_zip(self.export_src, dst_zip_file, args)
            else:
                self._copy_file_zip(self.export_src, dst_zip_file, args)

    def __copy_file_obj_zip(self, name: PurePosixPath | None, dest_path: PurePath,
                            dst_zip_file: zipfile.ZipFile, args: FileConstructionArguments):
        dest_path = str(dest_path)

        if self.is_dir(name):
            dst_zip_file.writestr(
                dest_path + '/', b'',
                args.compression, args.compresslevel
            )
        else:
            size, ctime = self.file_size(name), self.file_ctime(name)

            zinfo = zipfile.ZipInfo(dest_path, ctime or (1980, 1, 1, 0, 0, 0))
            zinfo.compress_type = args.compression
            zinfo._compresslevel = args.compresslevel
            zinfo.file_size = size

            with self.open(name) as src, dst_zip_file.open(zinfo, 'w') as dest:
                shutil.copyfileobj(src, dest)

    def _copy_file_zip(self: ElementMixinProtocol | Self, dest_path: PurePath,
                       dst_zip_file: zipfile.ZipFile, args: FileConstructionArguments):
        self.__copy_file_obj_zip(None, dest_path, dst_zip_file, args)

    def _copy_dir_zip(self: ElementMixinProtocol | Self, dest_path: PurePath,
                      dst_zip_file: zipfile.ZipFile, args: FileConstructionArguments):
        for name in self.iterdir(include_empty_root=True):
            self.__copy_file_obj_zip(name, (dest_path / name) if name else dest_path, dst_zip_file, args)

    def file_size(self: ElementMixinProtocol | Self, path: str | PurePosixPath | None = None) -> int | None:
        """ Get file size for the attachment.
        """
        if not self.has_attachment_content():
            raise FileNotFoundError(path)

        if self.is_dir(path):
            raise IsADirectoryError(path)

        try:
            if self.has_zip_bundle():
                with self.__zip_wrapper() as zip_file:
                    info = zip_file.getinfo(self.__get_zip_path(path))

                return info.file_size

            return self.__get_fs_path(path).stat().st_size

        except FileNotFoundError:
            raise FileNotFoundError(path) from None

    def file_ctime(self: ElementMixinProtocol | Self,
                   path: str | PurePosixPath | None = None) -> time.struct_time | None:
        """ Get file creation time for the attachment.
        """
        if not self.has_attachment_content():
            raise FileNotFoundError(path)

        try:
            if self.has_zip_bundle():
                with self.__zip_wrapper() as zip_file:
                    info = zip_file.getinfo(self.__get_zip_path(path))

                # ZipInfo.date_time is a 6-tuple. Convert it into a proper time.time_struct
                dt: tuple[int, int, int, int, int, int] = info.date_time
                try:
                    return time.localtime(time.mktime((dt[0], dt[1], dt[2], dt[3], dt[4], dt[5], -1, -1, -1)))
                except (ValueError, OverflowError):
                    return None

            return time.localtime(self.__get_fs_path(path).stat().st_ctime)

        except FileNotFoundError:
            raise FileNotFoundError(path) from None

    def file_hashes(self, hash_names: typing.Iterable[str]) -> dict[str, str]:
        """ Calculate the hashes of the file.

        Only for file attachments. Will return an empty dictionary if the file does not exist or is a directory.

        :param hash_names: Names of the hashes to calculate. Should be valid arguments to :py:func:`hashlib.new()`
        :return: A dictionary `hash-algorithm` -> `hash`
        """
        if self.is_dir():
            raise IsADirectoryError

        import hashlib
        hash_objects = {
            hn: hashlib.new(hn)
            for hn in hash_names
        }

        try:
            with self.open() as f:
                # Non-public const, but it will normally work, and otherwise fall back to a sane default
                bufsize = getattr(shutil, 'COPY_BUFSIZE', 64 * 1024)

                while True:
                    d = f.read(bufsize)
                    if d:
                        for hasher in hash_objects.values():
                            hasher.update(d)
                    else:
                        break

        except FileNotFoundError:
            raise FileNotFoundError from None

        else:
            return {
                hn: hash_obj.hexdigest()
                for hn, hash_obj in hash_objects.items()
            }

    def validate_hashes(self, expected_hashes: dict[str, str]) -> bool:
        """ Validate hash values of the file.

        Only for file attachments

        :param expected_hashes: A dictionary of `hash-algorithm` -> `hash` items
        :return: True of the hashes are the expected values
        """
        file_hashes = self.file_hashes(expected_hashes.keys())
        return file_hashes == expected_hashes

    # Exporting attachment into a bundle

    # noinspection PyProtectedMember
    def _export_path(self: ElementMixinProtocol | Self, path: PurePosixPath) \
            -> PurePosixPath:
        if self._orig_src is None:
            self._orig_src = path

            safe_path = PurePosixPath(
                pathvalidate.sanitize_filepath(
                    '/'.join(safe_path_name(part) for part in path.parts),
                    platform='universal', max_len=255
                )
            )

            index, export_src = 0, safe_path
            while True:
                try:
                    self.bundle._register_attachment_export_path(export_src)
                except FileExistsError:
                    index += 1
                    export_src = path.parent / f'{path.name}-{index}'
                else:
                    self._export_src = export_src
                    break

        else:
            assert self._orig_src == path, '`path` changed between calls'

        return self._export_src


AT = typing.TypeVar('AT', bound=SrcAttachmentMixin)


class SrcAttachmentsMixin(typing.Generic[AT]):
    # noinspection PyMethodMayBeStatic
    def _copy_to(self, attachments: typing.Sequence[AT], destination: Path, **kwargs):
        for attachment in attachments:
            attachment.copy_to(destination, **kwargs)
