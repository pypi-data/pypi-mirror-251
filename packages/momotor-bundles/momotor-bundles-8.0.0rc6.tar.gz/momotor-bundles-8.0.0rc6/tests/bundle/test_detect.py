import pathlib

import pytest

from bundle_test_helpers import parametrize_use_lxml
from momotor.bundles import Bundle, RecipeBundle, ProductBundle, ResultsBundle, InvalidBundle

FILES = pathlib.Path(__file__).parent / 'files'


@parametrize_use_lxml
@pytest.mark.parametrize(
    ['path', 'expected_result'],
    [
        pytest.param('full-recipe', RecipeBundle),
        pytest.param('product-2', ProductBundle),
        pytest.param('content.xml', ResultsBundle),
        pytest.param('huge_product.zip', ProductBundle),
        pytest.param('with-files.zip', RecipeBundle),
    ]
)
def test_detect_path(use_lxml, path, expected_result):
    assert Bundle.detect(FILES / path, use_lxml=use_lxml, legacy=False) is expected_result


@parametrize_use_lxml
@pytest.mark.parametrize(
    ['path'],
    [
        pytest.param('non-product-1.txt'),
        pytest.param('non-product-2.zip'),
    ]
)
def test_detect_invalid_path(use_lxml, path):
    with pytest.raises(InvalidBundle):
        Bundle.detect(FILES / path, use_lxml=use_lxml, legacy=False)


@parametrize_use_lxml
@pytest.mark.parametrize(
    ['path', 'expected_result'],
    [
        pytest.param('content.xml', ResultsBundle),
        pytest.param('huge_product.zip', ProductBundle),
        pytest.param('with-files.zip', RecipeBundle),
    ]
)
def test_detect_data(use_lxml, path, expected_result):
    assert Bundle.detect((FILES / path).read_bytes(), use_lxml=use_lxml, legacy=False) is expected_result


@parametrize_use_lxml
@pytest.mark.parametrize(
    ['path'],
    [
        pytest.param('non-product-1.txt'),
        pytest.param('non-product-2.zip'),
    ]
)
def test_detect_invalid_data(use_lxml, path):
    with pytest.raises(InvalidBundle):
        Bundle.detect((FILES / path).read_bytes(), use_lxml=use_lxml, legacy=False)


@parametrize_use_lxml
def test_detect_file_factory(use_lxml):
    bundle = Bundle.from_file_factory(FILES / 'product-1.xml', use_lxml=use_lxml, legacy=False)
    assert isinstance(bundle, ProductBundle)
    assert bundle.id == 'product-1'


@parametrize_use_lxml
def test_detect_bytes_factory(use_lxml):
    bundle = Bundle.from_bytes_factory((FILES / 'product-1.xml').read_bytes(), use_lxml=use_lxml, legacy=False)
    assert isinstance(bundle, ProductBundle)
    assert bundle.id == 'product-1'


@parametrize_use_lxml
def test_detect_factory_invalid_bundle(use_lxml):
    with pytest.raises(InvalidBundle):
        RecipeBundle.from_file_factory(FILES / 'product-1.xml', use_lxml=use_lxml, legacy=False)
