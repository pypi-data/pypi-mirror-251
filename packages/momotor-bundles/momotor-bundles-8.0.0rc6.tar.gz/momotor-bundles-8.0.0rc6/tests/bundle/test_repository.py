from pathlib import Path, PurePath

import pytest

from bundle_test_helpers import parametrize_use_lxml, listfiles
from momotor.bundles import RecipeBundle


def parametrize_bundle_path(f):
    return pytest.mark.parametrize(
        "bundle_path",
        [
            pytest.param('files/with-repository', id='directory bundle'),
            pytest.param('files/with-repository.zip', id='zip bundle'),
        ]
    )(f)


@parametrize_use_lxml
@parametrize_bundle_path
def test_direct_read(use_lxml, bundle_path):
    recipe_bundle = RecipeBundle.from_file_factory(Path(__file__).parent / bundle_path, use_lxml=use_lxml, legacy=False)
    repository = recipe_bundle.steps['step1'].checklet.repository

    assert repository.read('repofile.txt').strip() == b'File in repository'
    assert repository.read('subdir/repofile.txt').strip() == b'File in repository subdir'


@parametrize_use_lxml
@parametrize_bundle_path
def test_iterdir(use_lxml, bundle_path):
    recipe_bundle = RecipeBundle.from_file_factory(Path(__file__).parent / bundle_path, use_lxml=use_lxml, legacy=False)
    repository = recipe_bundle.steps['step1'].checklet.repository

    children = list(sorted(str(child) for child in repository.iterdir()))
    assert children == ['repofile.txt', 'subdir', 'subdir/repofile.txt']


@parametrize_use_lxml
@parametrize_bundle_path
def test_copy_to(use_lxml, bundle_path, tmp_path):
    recipe_bundle = RecipeBundle.from_file_factory(Path(__file__).parent / bundle_path, use_lxml=use_lxml, legacy=False)
    repository = recipe_bundle.steps['step1'].checklet.repository

    # Cannot copy to an existing directory
    with pytest.raises(FileExistsError):
        repository.copy_to(tmp_path)

    repository.copy_to(tmp_path, name='from_repo')
    assert sorted(listfiles(tmp_path)) == [
        (str(PurePath('from_repo/repofile.txt')), 'File in repository\n'),
        (str(PurePath('from_repo/subdir/repofile.txt')), 'File in repository subdir\n'),
    ]
