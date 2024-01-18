from pathlib import Path

import pytest

from momotor.bundles import ProductBundle, InvalidBundle
from momotor.bundles.exception import BundleLoadError, BundleFormatError

from bundle_test_helpers import parametrize_use_lxml


@parametrize_use_lxml
def test_direct_xml_file(use_lxml):
    path = Path(__file__).parent / 'files' / 'product-1.xml'

    bundle = ProductBundle.from_file_factory(path, use_lxml=use_lxml, legacy=False)

    assert bundle.id == 'product-1'
    assert bundle._base == path.parent
    assert bundle._zip_wrapper is None


@parametrize_use_lxml
def test_valid_directory(use_lxml):
    path = Path(__file__).parent / 'files' / 'product-2'

    bundle = ProductBundle.from_file_factory(path, use_lxml=use_lxml, legacy=False)

    assert bundle.id == 'product-2'
    assert bundle._base == path
    assert bundle._zip_wrapper is None


@parametrize_use_lxml
def test_valid_zip(use_lxml):
    path = Path(__file__).parent / 'files' / 'product-3.zip'

    bundle = ProductBundle.from_file_factory(path, use_lxml=use_lxml, legacy=False)

    assert bundle.id == 'product-3'
    assert bundle._base is None
    assert bundle._zip_wrapper is not None


@parametrize_use_lxml
def test_not_a_product(use_lxml):
    path = Path(__file__).parent / 'files' / 'recipe-1.xml'

    with pytest.raises(BundleFormatError,
                       match=r'Unexpected node \{http://momotor.org/1\.0\}recipe, '
                             r'expected \{http://momotor.org/1\.0\}product'):
        ProductBundle.from_file_factory(path, use_lxml=use_lxml, legacy=False)


@parametrize_use_lxml
def test_nonexistent_file(use_lxml):
    path = Path(__file__).parent / 'files' / 'product-0.xml'

    with pytest.raises(FileNotFoundError):
        ProductBundle.from_file_factory(path, use_lxml=use_lxml, legacy=False)


@parametrize_use_lxml
def test_not_an_xml_file(use_lxml):
    path = Path(__file__).parent / 'files' / 'non-product-1.txt'

    if use_lxml:
        exc = BundleLoadError
        msg = r'ElementTree not initialized, missing root'
    else:
        exc = BundleFormatError
        msg = r'syntax error'

    with pytest.raises(exc, match=msg):
        ProductBundle.from_file_factory(path, use_lxml=use_lxml, legacy=False)


@parametrize_use_lxml
def test_not_a_bundle_zip(use_lxml):
    path = Path(__file__).parent / 'files' / 'non-product-2.zip'

    with pytest.raises(InvalidBundle, match=r"A product bundle should contain a product\.xml file in the root"):
        ProductBundle.from_file_factory(path, use_lxml=use_lxml, legacy=False)


@parametrize_use_lxml
def test_inline_trailing_whitespace(use_lxml):
    path = Path(__file__).parent / 'files' / 'inline-trailing-whitespace.xml'

    bundle = ProductBundle.from_file_factory(path, use_lxml=use_lxml, legacy=False)

    assert bundle.id == 'inline-trailing-whitespace'
    assert bundle.files[0].read() == b'!   '
