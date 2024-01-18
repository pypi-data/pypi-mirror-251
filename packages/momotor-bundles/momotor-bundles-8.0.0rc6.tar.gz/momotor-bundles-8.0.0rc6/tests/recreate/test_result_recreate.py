import zipfile
from io import BytesIO
from pathlib import Path

import pytest

from bundle_test_helpers import NS, xml_to_dict, parametrize_use_lxml
from momotor.bundles import ResultsBundle
from momotor.bundles.const import BundleFormat


@pytest.mark.parametrize(
    "optimize",
    [
        pytest.param(True, id='optimize'),
        pytest.param(False, id='no optimize')
    ]
)
@parametrize_use_lxml
def test_result_merge(use_lxml, optimize):
    # Read the separate result bundles
    result1_bundle = ResultsBundle.from_file_factory(Path(__file__).parent / 'files' / 'result1', use_lxml=use_lxml, legacy=False)
    result2_bundle = ResultsBundle.from_file_factory(Path(__file__).parent / 'files' / 'result2', use_lxml=use_lxml, legacy=False)

    # Combine them into a results bundle
    combined_result_bundle = ResultsBundle()
    combined_results = [
        result1_bundle.results['step1'].recreate(combined_result_bundle),
        result2_bundle.results['step2'].recreate(combined_result_bundle),
    ]
    combined_result_bundle.create(results=combined_results)

    # Test it
    buffer = BytesIO()
    bundle_type = combined_result_bundle.to_buffer(
        buffer,
        sign_files=False, legacy=False,
        optimize=optimize, generator_name=False
    )

    assert BundleFormat.ZIP == bundle_type

    buffer.seek(0)
    with zipfile.ZipFile(buffer) as zf:
        assert ['result.xml', 'result/step1/result.txt', 'result/step2/result.txt'] == sorted(zf.namelist())

        expected_dom = {
            f'{NS}results': {
                # f'@{XSI_NS}schemaLocation': NS_LOCATION,
                f'{NS}result': [{
                    '@outcome': 'pass',
                    '@step': 'step1',
                    f'{NS}files': {
                        '@basesrc': 'result/step1',
                        f'{NS}file': [{
                            '@name': 'result.txt',
                            '@size': 29,
                        }, {
                            '@encoding': 'quopri',
                            '@name': 'other.txt',
                            '$': 'Other result for step 1',
                        }]
                    },
                    f'{NS}options': {
                        f'{NS}option': {
                            '@name': 'option',
                            '@value': 'value'
                        }
                    },
                    f'{NS}properties': {
                        f'{NS}property': {
                            '@name': 'property',
                            '@value': 'value'
                        }
                    },
                }, {
                    '@outcome': 'pass',
                    '@step': 'step2',
                    f'{NS}files': {
                        '@basesrc': 'result/step2',
                        f'{NS}file': [{
                            '@name': 'result.txt',
                            '@size': 29,
                        }, {
                            '@encoding': 'quopri',
                            '@name': 'other.txt',
                            '$': 'Other result for step 2',
                        }]
                    },
                    f'{NS}options': {
                        f'{NS}option': {
                            '@name': 'option',
                            '@value': 'value'
                        } if optimize else {
                            '$': 'value',
                            '@name': 'option'
                        }
                    },
                    f'{NS}properties': {
                        f'{NS}property': {
                            '@name': 'property',
                            '@value': 'value'
                        } if optimize else {
                            '$': 'value',
                            '@name': 'property'
                        }
                    }
                }]
            }
        }

        assert xml_to_dict(zf.read('result.xml')) == expected_dom

        assert b'This is the result of step 1' == zf.read('result/step1/result.txt').strip()
        assert b'This is the result of step 2' == zf.read('result/step2/result.txt').strip()
