import pytest

from momotor.bundles import ResultsBundle
from momotor.bundles.exception import BundleFormatError

from bundle_test_helpers import parametrize_use_lxml


@parametrize_use_lxml
def test_empty_results(use_lxml):
    msg = r"Document is empty" if use_lxml else r"no element found"

    with pytest.raises(BundleFormatError, match=msg):
        ResultsBundle.from_bytes_factory(b'', use_lxml=use_lxml, legacy=False)
