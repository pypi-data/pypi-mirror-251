from pathlib import Path

from momotor.bundles import ResultsBundle

from bundle_test_helpers import parametrize_use_lxml
from momotor.bundles.utils.arguments import BundleConstructionArguments


@parametrize_use_lxml
def test_no_binding_warnings_read(caplog, use_lxml):
    ResultsBundle.from_file_factory(Path(__file__).parent / 'files' / 'domnode.xml', use_lxml=use_lxml, legacy=False)
    for rec in caplog.records:
        assert 'Unable to convert DOM node' not in rec.message


@parametrize_use_lxml
def test_no_binding_warnings_write(caplog, use_lxml):
    bundle = ResultsBundle.from_file_factory(Path(__file__).parent / 'files' / 'domnode.xml', use_lxml=use_lxml, legacy=False)

    caplog.clear()
    new_bundle = ResultsBundle()
    new_bundle.create(id=None, results=[bundle.results['r1'].recreate(new_bundle)])
    new_bundle._to_xml(BundleConstructionArguments())
    for rec in caplog.records:
        assert 'Unable to convert DOM node' not in rec.message
