import operator
from pathlib import Path, PurePath, PurePosixPath

import pytest

from momotor.bundles import RecipeBundle

from bundle_test_helpers import parametrize_use_lxml, listfiles


def parametrize_bundle_path(f):
    return pytest.mark.parametrize(
        "bundle_path",
        [
            pytest.param('files/with-files', id='directory bundle'),
            pytest.param('files/with-files.zip', id='zip bundle'),
        ]
    )(f)


@parametrize_use_lxml
@parametrize_bundle_path
def test_open(use_lxml, bundle_path):
    recipe_bundle = RecipeBundle.from_file_factory(Path(__file__).parent / bundle_path, use_lxml=use_lxml, legacy=False)
    files = recipe_bundle.steps['step1'].files

    def _read_file(file_node):
        with file_node.open() as f:
            return f.read().strip()

    result = [
        _read_file(file_node) for file_node in files
    ]

    assert result == [
        b'This file is located in the root of the package',
        b'Base64 encoded content',
        b'This file is located in the root of the package',
        b'This file is located in a subdirectory',
        b'This file is located in subdirectory for step1',
        b'This file is located in the root of the step1 src',
        b'This file is located in the root of the package',
        b'Quopri encoded content',
        b'',
    ]


@parametrize_use_lxml
@parametrize_bundle_path
def test_file_copy_files(use_lxml, bundle_path, tmp_path):
    recipe_bundle = RecipeBundle.from_file_factory(Path(__file__).parent / bundle_path, use_lxml=use_lxml, legacy=False)
    recipe_bundle.steps['step1'].copy_files_to(tmp_path)

    assert sorted(listfiles(tmp_path)) == [
        (str(PurePath('also-in-subdir.txt')), 'This file is located in subdirectory for step1\n'),
        (str(PurePath('basedir', 'from-root.txt')), 'This file is located in the root of the step1 src\n'),
        (str(PurePath('file-in-root.txt')), 'This file is located in the root of the package\n'),
        (str(PurePath('in-subdir.txt')), 'This file is located in a subdirectory\n'),
        (str(PurePath('inline-base64.txt')), 'Base64 encoded content\n'),
        (str(PurePath('step1-file.txt')), 'This file is located in the root of the package\n'),
        (str(PurePath('step1', 'basedir', 'from-root.txt')), 'This file is located in the root of the package\n'),
        (str(PurePath('step1', 'empty.txt')), ''),
        (str(PurePath('step1', 'inline-quopri.txt')), 'Quopri encoded content\n'),
    ]


@parametrize_use_lxml
@parametrize_bundle_path
def test_file_ref(use_lxml, bundle_path):
    recipe_bundle = RecipeBundle.from_file_factory(Path(__file__).parent / bundle_path, use_lxml=use_lxml, legacy=False)
    files = recipe_bundle.steps['step1'].files

    result = [
        (file.name, file.src, file.class_, file.read().strip())
        for file in sorted(files, key=operator.attrgetter('name'))
    ]

    assert result == [
        (
            PurePosixPath('also-in-subdir.txt'), PurePosixPath('step1/subdir/file-in-dir.txt'), None,
            b'This file is located in subdirectory for step1'
        ),
        (
            PurePosixPath('basedir/from-root.txt'), PurePosixPath('step1/file-in-root.txt'), None,
            b'This file is located in the root of the step1 src'
        ),
        (
            PurePosixPath('file-in-root.txt'), PurePosixPath('file-in-root.txt'), 'files1',
            b'This file is located in the root of the package'
        ),
        (
            PurePosixPath('in-subdir.txt'), PurePosixPath('subdir/file-in-dir.txt'), 'step1.files1',
            b'This file is located in a subdirectory'
        ),
        (
            PurePosixPath('inline-base64.txt'), None, None,
            b'Base64 encoded content'
        ),
        (
            PurePosixPath('step1/basedir/from-root.txt'), PurePosixPath('file-in-root.txt'), None,
            b'This file is located in the root of the package'
        ),
        (
            PurePosixPath('step1/empty.txt'), None, None,
            b''
        ),
        (
            PurePosixPath('step1/inline-quopri.txt'), None, None,
            b'Quopri encoded content'
        ),
        (
            PurePosixPath('step1-file.txt'), PurePosixPath('file-in-root.txt'), None,
            b'This file is located in the root of the package'
        ),
    ]
