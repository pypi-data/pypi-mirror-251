from pathlib import Path

import pytest

from momotor.bundles import RecipeBundle

from bundle_test_helpers import parametrize_use_lxml


@parametrize_use_lxml
@pytest.mark.parametrize(['step_name', 'expected'], [
    ['step1', {
        'resource1': {'value1a', 'value1b'},
        'resource2': {'value2a', 'value2b'},
        'resource3': {'value3'},
    }],
    ['step2', {
        'resource1': {'value1a', 'value1b'},
        'resource2': {'value2a'},
    }],
    ['step3', {
        'resource4': {'value4'},
    }],
    ['step4', {
        'resource5': {'value5'},
        'resource6': {'value6'},
    }],
    ['step5', {
        'resource7': {'value7'},
    }],
    ['step6', {

    }],
])
def test_resource(step_name, expected, use_lxml):
    path = Path(__file__).parent / 'files' / 'resources.xml'

    recipe_bundle = RecipeBundle.from_file_factory(path, use_lxml=use_lxml, legacy=False)
    step_resources = recipe_bundle.steps[step_name].get_resources()

    result = {
        name: set(resource.value for resource in resources)
        for name, resources in step_resources.items()
    }

    assert result == expected
