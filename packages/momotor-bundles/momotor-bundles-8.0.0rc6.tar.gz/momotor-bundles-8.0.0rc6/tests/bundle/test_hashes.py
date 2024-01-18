import hashlib
from pathlib import PurePath

import pytest

from bundle_test_helpers import NS, xml_to_dict
from momotor.bundles import BundleHashError, ConfigBundle
from momotor.bundles.binding import FilesComplexType, FileComplexType, Config as ConfigRootType
from momotor.bundles.elements.files import File
from momotor.bundles.utils.arguments import BundleFactoryArguments, BundleConstructionArguments

TEST_TEXT = b'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
TEST_ALGO = ['sha1', 'sha256']
TEST_HASH = {
    algo: hashlib.new(algo, TEST_TEXT).hexdigest()
    for algo in TEST_ALGO
}


def _create_file(tmp_path, src):
    final_path = tmp_path / src
    final_path.parent.mkdir(parents=True)
    final_path.write_bytes(TEST_TEXT)
    return final_path


def _make_config_node(tmp_path, attributes) -> ConfigRootType:
    _create_file(tmp_path, PurePath('src/test.txt'))
    return ConfigRootType(
        files=[
            FilesComplexType(
                file=[
                    FileComplexType(
                        name='test.txt',
                        any_attributes=attributes
                    ),
                ],
                basesrc='src',
            ),
        ]
    )


@pytest.mark.parametrize(['attributes'], [
    pytest.param({'sha1': TEST_HASH['sha1']}, id='sha1'),
    pytest.param({'sha256': TEST_HASH['sha256']}, id='sha256'),
    pytest.param({'sha1': TEST_HASH['sha1'], 'sha256': TEST_HASH['sha256']}, id='sha1+sha256'),
    pytest.param({'not_a_hash': 'ignored'}, id='not a hash algorithm'),
])
def test_bundle_import_valid_hash(tmp_path, attributes):
    args = BundleFactoryArguments(validate_signature=True)
    cct = _make_config_node(tmp_path, attributes)

    try:
        ConfigBundle(tmp_path, None)._create_from_node(cct, args=args)
    except BundleHashError as e:
        pytest.fail(str(e))


@pytest.mark.parametrize(['attributes'], [
    pytest.param({'sha1': 'invalid'}, id='sha1 invalid'),
    pytest.param({'sha256': 'invalid'}, id='sha256 invalid'),
    pytest.param({'sha1': 'invalid', 'sha256': TEST_HASH['sha256']}, id='sha1+sha256, sha1 invalid'),
    pytest.param({'sha1': 'invalid', 'sha256': 'invalid'}, id='sha1+sha256, both invalid'),
])
def test_bundle_import_invalid_hash(tmp_path, attributes):
    args = BundleFactoryArguments(validate_signature=True)
    cct = _make_config_node(tmp_path, attributes)

    with pytest.raises(BundleHashError):
        ConfigBundle(tmp_path, None)._create_from_node(cct, args=args)


@pytest.mark.parametrize(['hashers'], [
    pytest.param(['sha1'], id='sha1'),
    pytest.param(['sha256'], id='sha256'),
    pytest.param(['sha1', 'sha256'], id='sha1+sha256'),
])
def test_bundle_create_hash(tmp_path, hashers):
    final_path = _create_file(tmp_path, PurePath('src/test.txt'))

    bundle = ConfigBundle()
    bundle.create(files=[
        File(bundle).create(
            name=final_path.name,
            src=final_path
        )
    ])

    attrs = xml_to_dict(
        bundle._to_xml(BundleConstructionArguments(sign_files=True, hashers=hashers, legacy=False)),
        f'{NS}config', f'{NS}files', f'{NS}file'
    )

    expected = {
        '@name': final_path.name,
        '@size': len(TEST_TEXT),
    }

    for algo in hashers:
        expected[f'@{algo}'] = TEST_HASH[algo]

    assert attrs == expected
