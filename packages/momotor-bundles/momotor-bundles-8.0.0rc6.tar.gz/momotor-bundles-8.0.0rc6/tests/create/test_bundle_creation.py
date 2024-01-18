import hashlib
from io import BytesIO
from pathlib import Path, PurePath

import typing
import zipfile

import pytest

from momotor.bundles import ResultsBundle, RecipeBundle
from momotor.bundles.binding import ResultComplexType, FilesComplexType, FileComplexType, OutcomeSimpleType, \
    Results as ResultsRootType
from momotor.bundles.const import BundleFormat
from momotor.bundles.elements.result import Result
from momotor.bundles.utils.arguments import BundleFactoryArguments

from bundle_test_helpers import NS, xml_to_dict, listfilenames, filehash, datahash


def test_result_bundle_without_attachments_creation():
    rct = ResultsRootType(
        result=[
            ResultComplexType(
                step='step',
                outcome=OutcomeSimpleType.PASS,
                files=[
                    FilesComplexType(
                        file=[
                            FileComplexType(
                                name='test2',
                                encoding='base64',
                                content=['aW5saW5lIGNvbnRlbnQK'],
                            ),
                        ],
                    ),
                ]
            ),
        ]
    )

    args = BundleFactoryArguments(validate_signature=False)
    bundle = ResultsBundle()._create_from_node(rct, args=args)

    buffer = BytesIO()
    bundle_type = bundle.to_buffer(buffer, sign_files=False, optimize=False, generator_name=False)

    assert BundleFormat.XML == bundle_type

    expected_dom = {
        f'{NS}results': {
            # f'@{XSI_NS}schemaLocation': NS_LOCATION,
            f'{NS}result': {
                '@outcome': 'pass',
                '@step': 'step',
                f'{NS}files': {
                    '@basesrc': 'result/step',
                    f'{NS}file': {
                        '@encoding': 'base64',
                        '@name': 'test2',
                        '$': 'aW5saW5lIGNvbnRlbnQK',
                    }
                }
            }
        }
    }

    buffer.seek(0)
    assert xml_to_dict(buffer.read()) == expected_dom


def test_result_bundle_forced_zip_creation():
    bundle = ResultsBundle()
    bundle.create(
        results=[
            Result(bundle).create(step_id='step', outcome='pass')
        ]
    )

    buffer = BytesIO()
    bundle_type = bundle.to_buffer(buffer, sign_files=False, zip=True)

    assert BundleFormat.ZIP == bundle_type

    buffer.seek(0)
    with zipfile.ZipFile(buffer) as zf:
        assert ['result.xml'] == zf.namelist()


def _create_complex_bundle(tmp_path):
    bundle_path = tmp_path / 'bundle'
    srcdir = bundle_path / 'src'
    srcdir.mkdir(parents=True)

    test_file_path = srcdir / 'test.txt'
    test_file_content = b'test file ' * 1000
    test_file_path.write_bytes(test_file_content)

    base64_content = 'aW5saW5lIGNvbnRlbnQK'

    rct = ResultsRootType(
        result=[
            ResultComplexType(
                step='step',
                outcome=OutcomeSimpleType.PASS,
                files=[
                    FilesComplexType(
                        file=[
                            FileComplexType(
                                name='test1',
                                src='test.txt',
                            ),
                            FileComplexType(
                                name='test2',
                                encoding='base64',
                                content=[base64_content],
                            ),
                        ],
                        basesrc='src'
                    ),
                ]
            ),
        ]
    )

    args = BundleFactoryArguments(validate_signature=False)

    expected_dom = {
        f'{NS}results': {
            # f'@{XSI_NS}schemaLocation': NS_LOCATION,
            f'{NS}result': {
                '@outcome': 'pass',
                '@step': 'step',
                f'{NS}files': {
                    '@basesrc': 'result/step',
                    f'{NS}file': [{
                        '@name': 'test1',
                        '@sha1': hashlib.sha1(test_file_content).hexdigest(),
                        '@size': len(test_file_content),
                    }, {
                        '@encoding': 'base64',
                        '@name': 'test2',
                        '$': base64_content,
                    }]
                }
            }
        }
    }

    # noinspection PyProtectedMember
    return ResultsBundle(bundle_path, None)._create_from_node(rct, args=args), expected_dom, test_file_content


def test_result_bundle_with_attachments_to_buffer(tmp_path):
    bundle, expected_dom, expected_file_content = _create_complex_bundle(tmp_path)

    buffer = BytesIO()
    bundle_type = bundle.to_buffer(buffer, sign_files=True, legacy=False, optimize=False, generator_name=False)

    assert BundleFormat.ZIP == bundle_type

    buffer.seek(0)
    with zipfile.ZipFile(buffer) as zf:
        assert sorted(zf.namelist()) == ['result.xml', 'result/step/test1']
        assert xml_to_dict(zf.read('result.xml')) == expected_dom
        assert zf.read('result/step/test1') == expected_file_content


def test_result_bundle_with_attachments_to_directory(tmp_path):
    bundle, expected_dom, expected_file_content = _create_complex_bundle(tmp_path)

    out_path = tmp_path / 'output'
    out_path.mkdir()

    bundle.to_directory(out_path, sign_files=True, legacy=False, optimize=False, generator_name=False)

    assert sorted(listfilenames(out_path)) == [
        str(PurePath('result.xml')),
        str(PurePath('result/step/test1'))
    ]
    assert xml_to_dict((out_path / 'result.xml').read_bytes()) == expected_dom
    assert (out_path / 'result/step/test1').read_bytes() == expected_file_content


def _dir_file_hash_set(base_path) -> set[str]:
    hashes = set()
    for fn in listfilenames(base_path):
        if fn != 'recipe.xml':
            fp = base_path / fn
            if not fp.is_dir():
                hashes.add(filehash(fp))

    return hashes


def _zip_file_hash_set(zip_data) -> set[str]:
    hashes = set()
    with zipfile.ZipFile(zip_data) as zf:
        for name in zf.namelist():
            if name != 'recipe.xml' and not name.endswith('/'):
                hashes.add(datahash(zf.read(name)))

    return hashes


@pytest.mark.parametrize(
    "method",
    [
        pytest.param('to_directory'),
        pytest.param('to_buffer')
    ]
)
def test_copy_recipe_with_checklet(tmp_path, method):
    path = Path(__file__).parent / 'files' / 'recipe'

    bundle = RecipeBundle.from_file_factory(path, legacy=False)

    if method == 'to_directory':
        out_path = tmp_path / 'output'
        out_path.mkdir()
        bundle.to_directory(out_path, sign_files=True, legacy=False)
        output_hashes = _dir_file_hash_set(out_path)
    else:
        out_buffer = BytesIO()
        bundle_type = bundle.to_buffer(out_buffer, sign_files=True, legacy=False)
        assert BundleFormat.ZIP == bundle_type
        output_hashes = _zip_file_hash_set(out_buffer)

    # Since the recipe can be rewritten and paths can change, we need to check that the same files have
    # been exported, but we cannot be certain of their location. So we calculate a set of hashes for all files
    # except the recipe.xml (which will be certainly be changed) and compare those

    recipe_hashes = _dir_file_hash_set(path)
    assert recipe_hashes == output_hashes
