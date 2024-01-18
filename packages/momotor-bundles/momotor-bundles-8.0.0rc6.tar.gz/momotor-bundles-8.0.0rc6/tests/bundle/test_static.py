import pytest

from momotor.bundles import Bundle, RecipeBundle, ConfigBundle, ProductBundle, ResultsBundle, TestResultBundle
from momotor.bundles.const import BundleCategory


@pytest.mark.parametrize(['bundle_class', 'tag', 'file_name', 'category'], [
    pytest.param(RecipeBundle, 'recipe', 'recipe.xml', BundleCategory.RECIPE),
    pytest.param(ConfigBundle, 'config', 'config.xml', BundleCategory.CONFIG),
    pytest.param(ProductBundle, 'product', 'product.xml', BundleCategory.PRODUCT),
    pytest.param(ResultsBundle, 'results', 'result.xml', BundleCategory.RESULTS),
    pytest.param(TestResultBundle, 'testresult', 'result.xml', BundleCategory.TEST_RESULTS),
])
def test_bundles_statics(bundle_class: Bundle, tag: str, file_name: str, category: BundleCategory):
    assert tag == bundle_class.get_root_tag()
    assert file_name == bundle_class.get_default_xml_name()
    assert category == bundle_class.get_category()
