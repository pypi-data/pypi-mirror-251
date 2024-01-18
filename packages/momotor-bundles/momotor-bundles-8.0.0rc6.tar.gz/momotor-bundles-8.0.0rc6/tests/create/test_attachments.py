import tempfile
import zipfile
from io import BytesIO
from pathlib import Path, PurePosixPath

import pytest

from bundle_test_helpers import xml_to_dict, NS
from momotor.bundles import ConfigBundle, ResultsBundle
from momotor.bundles.elements.files import File


def test_missing_relative_attachments(tmp_path):
    bundle = ConfigBundle(tmp_path, None)

    with pytest.raises(FileNotFoundError):
        File(bundle).create(src=PurePosixPath('doesnotexist'))


def test_missing_absolute_attachments(tmp_path):
    bundle = ConfigBundle(None, None)

    with pytest.raises(FileNotFoundError):
        File(bundle).create(src=tmp_path / 'doesnotexist')


def test_safe_src(tmp_path):
    unsafe_filename = "File with \u00fcns\u00e5fe ch\u00e2ract\u00ebrs \u263a.txt"

    test_file = tmp_path / unsafe_filename
    test_file.write_bytes(b'*'*1024*64)

    bundle = ConfigBundle()
    bundle.create(
        files=[
            File(bundle).create(name=unsafe_filename, src=test_file)
        ]
    )

    buffer = BytesIO()
    bundle.to_buffer(buffer, zip=True, legacy=False)
    with zipfile.ZipFile(buffer) as zf:
        xml = zf.read(bundle.get_default_xml_name())
        files_node = xml_to_dict(xml, f'{NS}config', f'{NS}files')
        file_node = files_node[f'{NS}file']

        base_src = files_node.get('@basesrc')
        file_name = file_node['@name']
        file_src = file_node.get('@src', file_name)

        # Test that the `name` attribute is the original name
        assert file_name == unsafe_filename

        # Test that the file in the zip exists
        src_path = str(PurePosixPath(base_src) / file_src) if base_src else file_src
        assert src_path in zf.namelist()

        # Test that the `src` attribute is pure ASCII (if not, this will raise UnicodeEncodeError)
        assert file_src.encode('ascii') == file_src.encode('utf-8')


def test_missing_on_import():
    path = Path(__file__).parent / 'files' / 'missing_attachment'

    with pytest.raises(FileNotFoundError):
        ConfigBundle.from_file_factory(path, legacy=False)


def test_missing_on_import_allowed():
    path = Path(__file__).parent / 'files' / 'missing_attachment'

    config = ConfigBundle.from_file_factory(path, validate_signature=False, legacy=False)

    assert len(config.files) == 1
    assert str(config.files[0].name) == 'missing'

    with pytest.raises(FileNotFoundError):
        config.files[0].open()


def test_has_inline_content():
    bundle = ResultsBundle()
    file = File(bundle).create(
        name='inline-file',
        content=b'content'
    )

    assert file.has_inline_content()


def test_create_directory_attachments():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        (tmpdir / 'test.txt').write_bytes(b'test')
        (tmpdir / '.hidden.txt').write_bytes(b'hidden')

        (tmpdir / 'subdir').mkdir()
        (tmpdir / 'subdir' / 'test.txt').write_bytes(b'subdir-test')
        (tmpdir / 'subdir' / '.hidden.txt').write_bytes(b'subdir-hidden')

        (tmpdir / '.hidden').mkdir()
        (tmpdir / '.hidden' / 'test.txt').write_bytes(b'hidden-test')
        (tmpdir / '.hidden' / '.hidden.txt').write_bytes(b'hidden-hidden')

        (tmpdir / 'empty').mkdir()

        bundle = ConfigBundle()
        file = File(bundle).create(name='testdir', src=tmpdir)

        assert file.is_dir()
        assert file.read('test.txt') == b'test'
        assert file.read('.hidden.txt') == b'hidden'
        assert file.read('subdir/test.txt') == b'subdir-test'
        assert file.read('subdir/.hidden.txt') == b'subdir-hidden'
        assert file.read('.hidden/test.txt') == b'hidden-test'
        assert file.read('.hidden/.hidden.txt') == b'hidden-hidden'
        assert file.is_dir('empty')

        bundle.create(id='dirtest', files=[file],)

        buffer = BytesIO()
        bundle.to_buffer(buffer, zip=True, legacy=False, sign_files=True, hashers=['sha1'])
        with zipfile.ZipFile(buffer) as zf:
            zipfiles = set(zf.namelist())

            xml = zf.read(bundle.get_default_xml_name())
            files_node = xml_to_dict(xml, f'{NS}config', f'{NS}files')
            file_node = files_node.get(f'{NS}file')

            assert file_node is not None
            assert '@size' not in file_node
            assert '@sha1' not in file_node

            file_name = file_node.get('@name')
            assert file_name == 'testdir'

            base_src = files_node.get('@basesrc')
            file_path = PurePosixPath(base_src) / file_node.get('@src', file_name)
            assert zf.read(str(file_path / 'test.txt')) == b'test'
            assert zf.read(str(file_path / '.hidden.txt')) == b'hidden'
            assert zf.read(str(file_path / 'subdir/test.txt')) == b'subdir-test'
            assert zf.read(str(file_path / 'subdir/.hidden.txt')) == b'subdir-hidden'
            assert zf.read(str(file_path / '.hidden/test.txt')) == b'hidden-test'
            assert zf.read(str(file_path / '.hidden/.hidden.txt')) == b'hidden-hidden'
            assert str(file_path / 'empty') + '/' in zipfiles

        with tempfile.TemporaryDirectory() as dstdir:
            dstdir = Path(dstdir)

            # Test that content is propertly created
            bundle.to_directory(dstdir)
            with open(dstdir / bundle.get_default_xml_name(), 'rb') as xml:
                files_node = xml_to_dict(xml.read(), f'{NS}config', f'{NS}files')
                file_node = files_node.get(f'{NS}file')

                assert file_node is not None
                assert '@size' not in file_node
                assert '@sha1' not in file_node

                file_name = file_node.get('@name')
                assert file_name == 'testdir'

                base_src = files_node.get('@basesrc')
                file_path = PurePosixPath(base_src) / file_node.get('@src', file_name)
                assert (dstdir / file_path / 'test.txt').read_bytes() == b'test'
                assert (dstdir / file_path / '.hidden.txt').read_bytes() == b'hidden'
                assert (dstdir / file_path / 'subdir/test.txt').read_bytes() == b'subdir-test'
                assert (dstdir / file_path / 'subdir/.hidden.txt').read_bytes() == b'subdir-hidden'
                assert (dstdir / file_path / '.hidden/test.txt').read_bytes() == b'hidden-test'
                assert (dstdir / file_path / '.hidden/.hidden.txt').read_bytes() == b'hidden-hidden'
                assert (dstdir / file_path / 'empty').exists()


def test_empty_directory_attachment():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        bundle = ConfigBundle()
        file = File(bundle).create(name='emptydir', src=tmpdir)
        assert file.is_dir()
        bundle.create(id='emptydirtest', files=[file],)

        # Test that empty directory is properly created in zip export
        buffer = BytesIO()
        bundle.to_buffer(buffer, zip=True, legacy=False, sign_files=True, hashers=['sha1'])
        with zipfile.ZipFile(buffer) as zf:
            zipfiles = set(zf.namelist())

            xml = zf.read(bundle.get_default_xml_name())
            files_node = xml_to_dict(xml, f'{NS}config', f'{NS}files')
            file_node = files_node.get(f'{NS}file')

            assert file_node is not None
            assert '@size' not in file_node
            assert '@sha1' not in file_node

            file_name = file_node.get('@name')
            assert file_name == 'emptydir'

            base_src = files_node.get('@basesrc')
            file_path = PurePosixPath(base_src) / file_node.get('@src', file_name)
            assert str(file_path) + '/' in zipfiles

        with tempfile.TemporaryDirectory() as dstdir:
            dstdir = Path(dstdir)

            # Test that empty directory is properly created in directory export
            bundle.to_directory(dstdir)
            with open(dstdir / bundle.get_default_xml_name(), 'rb') as xml:
                files_node = xml_to_dict(xml.read(), f'{NS}config', f'{NS}files')
                file_node = files_node.get(f'{NS}file')

                assert file_node is not None
                assert '@size' not in file_node
                assert '@sha1' not in file_node

                file_name = file_node.get('@name')
                assert file_name == 'emptydir'

                base_src = files_node.get('@basesrc')
                file_path = PurePosixPath(base_src) / file_node.get('@src', file_name)
                assert (dstdir / file_path).is_dir()
