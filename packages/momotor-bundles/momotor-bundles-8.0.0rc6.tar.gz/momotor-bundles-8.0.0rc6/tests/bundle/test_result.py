import pytest

from momotor.bundles import ResultsBundle
from momotor.bundles.elements.result import Result
from bundle_test_helpers import NS, XSI_NS, NS_LOCATION, xml_to_dict


# noinspection PyProtectedMember
from momotor.bundles.utils.arguments import BundleConstructionArguments


def test_result_create():
    # noinspection PyTypeChecker
    result = ResultsBundle()
    result.create(
        results=[
            Result(result).create(step_id='step1', outcome='pass')
        ]
    )

    expected_dom = {
        f'{NS}results': {
            # f'@{XSI_NS}schemaLocation': NS_LOCATION,
            f'{NS}result': {'@outcome': 'pass', '@step': 'step1'}
        }
    }

    assert xml_to_dict(
        result._to_xml(
            BundleConstructionArguments(generator_name=False)
        )
    ) == expected_dom


@pytest.mark.parametrize(['outcome', 'propname'], [
    pytest.param('pass', 'passed', id='pass'),
    pytest.param('fail', 'failed', id='fail'),
    pytest.param('error', 'erred', id='error'),
])
def test_result_outcome(outcome, propname):
    # noinspection PyTypeChecker
    result = Result(ResultsBundle()).create(step_id='step1', outcome=outcome)
    assert outcome == result.outcome
    for prop in ['passed', 'failed', 'erred']:
        assert (propname == prop) is getattr(result, prop)
