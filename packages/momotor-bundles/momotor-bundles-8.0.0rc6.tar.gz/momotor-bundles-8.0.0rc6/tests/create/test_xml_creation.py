import pytest

from bundle_test_helpers import NS, xml_to_dict, parametrize_use_lxml
from momotor.bundles import ResultsBundle
from momotor.bundles.binding import ResultComplexType, FilesComplexType, FileComplexType, Results as ResultsRootType, \
    OutcomeSimpleType
from momotor.bundles.elements.files import File
from momotor.bundles.elements.properties import Property
from momotor.bundles.elements.result import Result
from momotor.bundles.utils.arguments import BundleConstructionArguments, BundleFactoryArguments


@parametrize_use_lxml
@pytest.mark.parametrize(
    "pretty_xml",
    [
        pytest.param(True),
        pytest.param(False)
    ]
)
def test_result_node_xml_creation(pretty_xml, use_lxml):
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
                                src='test1',
                            ),
                            FileComplexType(
                                name='test2',
                                encoding='base64',
                                content=['aW5saW5lIGNvbnRlbnQK'],
                            ),
                        ],
                        basesrc='src',
                    )
                ],
            )
        ]
    )

    args = BundleFactoryArguments(validate_signature=False)
    bundle = ResultsBundle(None, None)._create_from_node(rct, args=args)

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
                    }, {
                        '@encoding': 'base64',
                        '@name': 'test2',
                        '$': 'aW5saW5lIGNvbnRlbnQK',
                    }]
                }
            }
        }
    }

    generated_xml = bundle._to_xml(
        BundleConstructionArguments(use_lxml=use_lxml, pretty_xml=bool(pretty_xml), sign_files=False,
                                    legacy=False, optimize=False, generator_name=False)
    )

    assert xml_to_dict(generated_xml) == expected_dom


@parametrize_use_lxml
@pytest.mark.parametrize(
    "pretty_xml",
    [
        pytest.param(True),
        pytest.param(False)
    ]
)
def test_result_bundle_xml_creation_from_bundle(pretty_xml, use_lxml):
    bundle = ResultsBundle(None, None)
    bundle.create(
        results=[
            Result(bundle).create(
                step_id='step',
                outcome='pass',
                properties=[
                    Property(bundle).create(
                        name='test1',
                        value='{{{HTML[<h5>some content</h5>]}}}',
                    ),
                    Property(bundle).create(
                        name='test2',
                        value='another property'
                    )
                ]
            )
        ]
    )

    expected_dom = {
        f'{NS}results': {
            # f'@{XSI_NS}schemaLocation': NS_LOCATION,
            f'{NS}result': {
                '@outcome': 'pass',
                '@step': 'step',
                f'{NS}properties': {
                    f'{NS}property': [{
                        '@name': 'test1',
                        '@value': '{{{HTML[<h5>some content</h5>]}}}',
                    }, {
                        '@name': 'test2',
                        '@value': 'another property',
                    }]
                }
            }
        }
    }

    generated_xml = bundle._to_xml(
        BundleConstructionArguments(use_lxml=use_lxml, pretty_xml=bool(pretty_xml), generator_name=False)
    )

    assert xml_to_dict(generated_xml) == expected_dom


@parametrize_use_lxml
def test_legacy_option(tmp_path, use_lxml):
    src_dir = tmp_path / 'src'
    src_dir.mkdir()
    src_path = src_dir / 'test.txt'
    test_content = 'test file'
    src_path.write_text(test_content)

    bundle = ResultsBundle(None, None)
    bundle.create(
        results=[
            Result(bundle).create(
                step_id='step',
                outcome='pass',
                files=[
                    File(bundle).create(name='test.txt', src=src_path)
                ]
            )
        ]
    )

    expected_current_dom = {
        f'{NS}results': {
            # f'@{XSI_NS}schemaLocation': NS_LOCATION,
            f'{NS}result': {
                '@outcome': 'pass',
                '@step': 'step',
                f'{NS}files': {
                    '@basesrc': 'result/step',
                    f'{NS}file': {
                        '@name': 'test.txt',
                        '@size': len(test_content),
                    }
                }
            }
        }
    }

    generated_current_xml = bundle._to_xml(
        BundleConstructionArguments(use_lxml=use_lxml, sign_files=False, legacy=False, generator_name=False)
    )

    assert xml_to_dict(generated_current_xml) == expected_current_dom

    expected_legacy_dom = {
        f'{NS}results': {
            # f'@{XSI_NS}schemaLocation': NS_LOCATION,
            f'{NS}result': {
                '@outcome': 'pass',
                '@step': 'step',
                f'{NS}files': {
                    '@basesrc': 'result/step',
                    f'{NS}file': {
                        '@name': 'test.txt',
                        '@src': 'test.txt',
                        '@size': len(test_content),
                    }
                }
            }
        }
    }

    generated_legacy_xml = bundle._to_xml(
        BundleConstructionArguments(use_lxml=use_lxml, sign_files=False, legacy=True, generator_name=False)
    )

    assert xml_to_dict(generated_legacy_xml) == expected_legacy_dom
