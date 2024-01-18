from pathlib import Path

from momotor.bundles.product import ProductBundle

from bundle_test_helpers import parametrize_use_lxml


@parametrize_use_lxml
def test_huge_file_lxml(use_lxml):
    product = ProductBundle.from_file_factory(
        Path(__file__).parent / 'files' / 'huge_product.zip', use_lxml=use_lxml, legacy=False
    )

    assert len(product.files[0].value) > 10000000
