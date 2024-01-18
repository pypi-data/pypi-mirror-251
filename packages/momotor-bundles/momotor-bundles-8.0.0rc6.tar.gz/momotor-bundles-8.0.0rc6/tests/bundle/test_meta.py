from __future__ import annotations

import typing
from pathlib import Path

import pytest

from momotor.bundles import RecipeBundle, ResultsBundle
from momotor.bundles.elements.meta import default_generator, Meta, Description
from momotor.bundles.exception import BundleFormatError

from bundle_test_helpers import NS, XML_NS, xml_to_dict
from momotor.bundles.utils.arguments import BundleConstructionArguments


def test_meta_factory():
    recipe = RecipeBundle.from_file_factory(
        Path(__file__).parent / 'files' / 'meta' / 'recipe-with-meta.xml', legacy=False
    )

    meta = recipe.meta

    assert meta.name == 'Recipe with meta'
    assert meta.version == '1.0'
    assert meta.authors == tuple(['momotor'])
    assert meta.generators == tuple(['lorem', 'ipsum'])
    assert meta.sources == tuple()

    assert len(meta.descriptions) == 2

    assert meta.descriptions[0].text == 'Recipe with meta'
    assert meta.descriptions[0].lang is None

    assert meta.descriptions[1].text == 'Description <i>with</i> <b>HTML</b>'
    assert meta.descriptions[1].lang == 'en'


@pytest.mark.parametrize([
    'validate_xml', 'legacy'
], [
    pytest.param(True, False),
    pytest.param(True, True),
    pytest.param(False, False),
    pytest.param(False, True),
])
def test_meta_invalid_description(validate_xml, legacy):
    """ Test invalid description containing XML entities """
    if validate_xml and not legacy:
        # if validation is enabled and the legacy flag is not set, it should raise an error
        expected = pytest.raises(BundleFormatError, match=r'Incorrectly formatted meta-description')
    else:
        # otherwise, it should warn
        expected = pytest.warns(UserWarning,  match=r'Incorrectly formatted meta-description')

    with expected:
        RecipeBundle.from_file_factory(
            Path(__file__).parent / 'files' / 'meta' / 'invalid-description.xml',
            validate_xml=validate_xml, legacy=legacy
        )


@pytest.mark.parametrize([
    'generator_name', 'expected_value'
], [
    pytest.param(False, None),
    pytest.param(True, '{}'),
    pytest.param('test', 'test ({})'),
])
def test_meta_generator(generator_name: str, expected_value: str | None):
    default_generator_name = default_generator()

    result = ResultsBundle()
    result.create(id='result')

    expected_dom = {
        f'{NS}results': {
            '@id': 'result',
            **({
                f'{NS}meta': {
                    f'{NS}generator': {'$': expected_value.format(default_generator_name)}
                }
            } if expected_value else {})
        }
    }

    assert xml_to_dict(
        result._to_xml(
            BundleConstructionArguments(generator_name=generator_name)
        )
    ) == expected_dom


def test_meta_create():
    result = ResultsBundle()
    result.create(
        id='result',
        meta=Meta(
            name='meta-test',
            version='1.0',
            descriptions=[
                Description(result).create(
                    text='description 1',
                ),
                Description(result).create(
                    text='description 2',
                    lang='en',
                ),
            ],
            authors=('author 1', 'author 2'),
            sources=('source 1', 'source 2'),
            generators=('generator 1', 'generator 2'),
        )
    )

    expected_dom = {
        f'{NS}results': {
            '@id': 'result',
            f'{NS}meta': {
                f'{NS}name': {'$': 'meta-test'},
                f'{NS}version': {'$': 1.0},
                f'{NS}description': [
                    {'$': 'description 1'},
                    {'$': 'description 2', f'@{XML_NS}lang': 'en'},
                ],
                f'{NS}author': [
                    {'$': 'author 1'},
                    {'$': 'author 2'},
                ],
                f'{NS}source': [
                    {'$': 'source 1'},
                    {'$': 'source 2'},
                ],
                f'{NS}generator': [
                    {'$': 'generator 1'},
                    {'$': 'generator 2'},
                ],
            }
        }
    }

    assert xml_to_dict(
        result._to_xml(
            BundleConstructionArguments(generator_name=False)
        )
    ) == expected_dom


def test_multiple_meta_factory():
    with pytest.warns(UserWarning) as warnings:
        recipe = RecipeBundle.from_file_factory(
            Path(__file__).parent / 'files' / 'meta' / 'recipe-with-multiple-meta.xml', legacy=False
        )

    assert set(w.message.args[0] for w in warnings) == {
        'Multiple `meta.name` elements, using first one',
        'Multiple `meta.version` elements, using first one'
    }

    meta = recipe.meta

    assert meta.name == 'name 1'
    assert meta.version == '1.0'
    assert meta.authors == tuple(['author 1', 'author 2'])
    assert meta.generators == tuple(['generator 1', 'generator 2'])
    assert meta.sources == tuple()

    assert len(meta.descriptions) == 2
    assert meta.descriptions[0].text == 'description 1'
    assert meta.descriptions[1].text == 'description 2'
