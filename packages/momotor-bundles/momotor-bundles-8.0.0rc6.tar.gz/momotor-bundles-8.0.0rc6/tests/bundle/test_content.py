import base64
from pathlib import Path

import pytest

from bundle_test_helpers import NS, xml_to_dict, mark_skipif_no_lxml
from bundle_test_helpers import parametrize_use_lxml
from momotor.bundles import ResultsBundle, ConfigBundle
from momotor.bundles.elements.content import ContentBasicElement, NO_CONTENT, NoContent
from momotor.bundles.elements.options import Option
from momotor.bundles.test import TestBundle, TestContentFullElement, TestContentBasicElement
from momotor.bundles.utils.arguments import BundleConstructionArguments
from momotor.bundles.utils.encoding import decode_data
from momotor.bundles.utils.encoding import quopri_encode

max_value_string = 'x' * ContentBasicElement.MAX_VALUE_LENGTH
child_content_string = 'x' * (ContentBasicElement.MAX_VALUE_LENGTH + 1)


@pytest.mark.parametrize(
    ['value', 'expected_raw_content', 'expected_value', 'expected_encoding', 'expected_type'],
    [
        pytest.param(
            'short string',
            None,
            'short string',
            None,
            None,
            id='short string'
        ),

        pytest.param(
            max_value_string,
            None,
            max_value_string,
            None,
            None,
            id='max value length string'
        ),

        pytest.param(
            child_content_string,
            (quopri_encode(child_content_string),),
            None,
            'quopri',
            None,
            id='string too long for value'
        ),

        pytest.param(
            'newline terminated\n',
            (quopri_encode('newline terminated\n'),),
            None,
            'quopri',
            None,
            id='quopri',
        ),

        pytest.param(
            '\x00',
            (base64.b64encode(b'\x00').decode('utf-8'),),
            None,
            'base64',
            None,
            id='base64',
        ),

        pytest.param(
            b'bytes',
            (quopri_encode('bytes'),),
            None,
            'quopri',
            None,
            id='bytes',
        ),

        pytest.param(
            True,
            (True,),
            None,
            None,
            None,
            id='boolean true',
        ),

        pytest.param(
            False,
            (False,),
            None,
            None,
            None,
            id='boolean false',
        ),

        pytest.param(
            None,
            (None,),
            None,
            None,
            None,
            id='none',
        ),

        pytest.param(
            1,
            None,
            '1',
            None,
            'integer',
            id='integer',
        ),

        pytest.param(
            0.5,
            None,
            '0.5',
            None,
            'float',
            id='float',
        ),

        pytest.param(
            NO_CONTENT,
            None,
            None,
            None,
            None,
            id='missing content'
        ),
    ]
)
def test_content_create_raw_content(
        value,
        expected_raw_content, expected_value, expected_encoding, expected_type
):
    bundle = TestBundle()
    content = TestContentFullElement(bundle)
    content.value = value

    if value is NO_CONTENT:
        assert content._processed_value is None
    else:
        assert content._processed_value == (value,)

    content._create_raw_content()
    assert content._raw_content == expected_raw_content
    assert content._value == expected_value
    assert content._encoding == expected_encoding
    assert content._type == expected_type


@pytest.mark.parametrize(
    ['value', 'expected'],
    [
        pytest.param('\x00', ValueError, id='requiring encoding'),
        pytest.param(b'bytes', TypeError, id='bytes'),
        pytest.param(1, TypeError, id='integer'),
        pytest.param(0.5, TypeError, id='float'),
    ]
)
def test_basic_content_value_error(value, expected):
    bundle = TestBundle()
    content = TestContentBasicElement(bundle)
    with pytest.raises(expected):
        content.value = value


@pytest.mark.parametrize(
    ['raw_content', 'value', 'encoding', 'type_', 'expected'],
    [
        pytest.param(
            None,
            'short string',
            None,
            None,
            ('short string', None),
            id='short string'
        ),

        pytest.param(
            None,
            max_value_string,
            None,
            None,
            (max_value_string, None),
            id='max value length string'
        ),

        pytest.param(
            ('short child content string',),
            None,
            None,
            'text/plain',
            ('short child content string', 'text/plain'),
            id='short child content string'
        ),

        pytest.param(
            (quopri_encode(child_content_string),),
            None,
            'quopri',
            None,
            (child_content_string.encode('utf-8'), None),
            id='string too long for value'
        ),

        pytest.param(
            (quopri_encode('newline terminated\n'),),
            None,
            'quopri',
            None,
            (b'newline terminated\n', None),
            id='quopri',
        ),

        pytest.param(
            (base64.b64encode(b'\x00').decode('utf-8'),),
            None,
            'base64',
            'text/null',
            (b'\x00', 'text/null'),
            id='base64',
        ),

        pytest.param(
            (quopri_encode('bytes'),),
            None,
            'quopri',
            'text/plain',
            (b'bytes', 'text/plain'),
            id='bytes',
        ),

        pytest.param(
            (True,),
            None,
            None,
            None,
            (True, None),
            id='boolean true',
        ),

        pytest.param(
            (False,),
            None,
            None,
            None,
            (False, None),
            id='boolean false',
        ),

        pytest.param(
            (None,),
            None,
            None,
            None,
            (None, None),
            id='none',
        ),

        pytest.param(
            None,
            '1',
            None,
            'integer',
            (1, None),
            id='integer',
        ),

        pytest.param(
            None,
            '0.5',
            None,
            'float',
            (0.5, None),
            id='float',
        ),
    ]
)
def test_content_process_value(raw_content, encoding, value, type_, expected):
    bundle = TestBundle()
    content = TestContentFullElement(bundle)

    content._raw_content = raw_content
    content._encoding = encoding
    content._value = value
    content._type = type_

    content._content_set = True
    content._type_set = True

    assert content._process_value() == expected


def _test_options(bundle: ResultsBundle):
    result = bundle.results['r1']

    true_option = result.get_option_value('is-true')
    assert true_option is True

    false_option = result.get_option_value('is-false')
    assert false_option is False

    null_option = result.get_option_value('is-none')
    assert null_option is None

    int_option = result.get_option_value('is-int')
    assert isinstance(int_option, int) and int_option == 1

    float_option = result.get_option_value('is-float')
    assert isinstance(float_option, float) and float_option == 0.5

    value_str_option = result.get_option_value('is-value-string')
    assert value_str_option == 'test'

    content_str_option = result.get_option_value('is-content-string')
    assert content_str_option.strip() == 'test'

    base64_option = result.get_option_value('is-base64')
    assert base64_option == b'test\n'

    quopri_option = result.get_option_value('is-quopri')
    assert quopri_option == b'test\n'

    with pytest.raises(NoContent):
        result.get_option_value('is-empty')

    with pytest.raises(KeyError):
        result.get_option_value('does-not-exist')


@parametrize_use_lxml
def test_read_content(use_lxml):
    """ Test that options are read correctly """
    path = Path(__file__).parent / 'files' / 'content.xml'
    bundle = ResultsBundle.from_file_factory(path, use_lxml=use_lxml, legacy=False)
    _test_options(bundle)


@parametrize_use_lxml
def test_recreate_content(use_lxml):
    """ Test that recreating options produces identical values (but the XML could be different)
    """
    path = Path(__file__).parent / 'files' / 'content.xml'
    bundle = ResultsBundle.from_file_factory(path, use_lxml=use_lxml, legacy=False)
    _test_options(bundle)

    new_bundle = ResultsBundle()
    new_bundle.create(results=[bundle.results['r1'].recreate(new_bundle)])
    _test_options(new_bundle)


# noinspection PyProtectedMember
@pytest.mark.parametrize(['use_lxml_read', 'use_lxml_write', 'pretty_xml'], [
    pytest.param(True, True, True, marks=mark_skipif_no_lxml),
    pytest.param(True, True, False, marks=mark_skipif_no_lxml),
    pytest.param(True, False, True, marks=mark_skipif_no_lxml),
    pytest.param(True, False, False, marks=mark_skipif_no_lxml),
    pytest.param(False, True, True, marks=mark_skipif_no_lxml),
    pytest.param(False, True, False, marks=mark_skipif_no_lxml),
    pytest.param(False, False, True),
    pytest.param(False, False, False),
])
def test_rewrite_content(use_lxml_read: bool, use_lxml_write: bool, pretty_xml: bool):
    """ Test that read-write-read cycle of XML without recoding produces identical values
    """
    path = Path(__file__).parent / 'files' / 'content.xml'
    bundle = ResultsBundle.from_file_factory(path, use_lxml=use_lxml_read, legacy=False)
    _test_options(bundle)

    xml = bundle._to_xml(BundleConstructionArguments(pretty_xml=pretty_xml, use_lxml=use_lxml_write,
                                                     legacy=False, optimize=False))
    new_bundle = ResultsBundle.from_bytes_factory(xml, legacy=False)
    _test_options(new_bundle)


@pytest.mark.parametrize(('create_args', 'expected'), [
    pytest.param(
        dict(name='is-true', value=True),
        {'@name': 'is-true', f'{NS}true': {}},
        id='true'
    ),
    pytest.param(
        dict(name='is-false', value=False),
        {'@name': 'is-false', f'{NS}false': {}},
        id='false'
    ),
    pytest.param(
        dict(name='is-none', value=None),
        {'@name': 'is-none', f'{NS}none': {}},
        id='none'
    ),
    pytest.param(
        dict(name='is-int', value=1),
        {'@name': 'is-int', '@type': 'integer', '@value': 1},
        id='int'
    ),
    pytest.param(
        dict(name='is-float', value=0.5),
        {'@name': 'is-float', '@type': 'float', '@value': 0.5},
        id='float'
    ),
    pytest.param(
        dict(name='is-short-string', value="test"),
        {'@name': 'is-short-string', '@value': 'test'},
        id='short string'
    ),
    pytest.param(
        dict(name='is-printable-bytes', value=b'test'),
        {'@name': 'is-printable-bytes', '@encoding': 'quopri', '$': 'test'},
        id='printable bytes'
    ),
    pytest.param(
        dict(name='is-unprintable-bytes', value=b'\x00\xff'),
        {'@name': 'is-unprintable-bytes', '@encoding': 'base64', '$': 'AP8='},
        id='unprintable bytes'
    ),

    # No value is written as a <none/> node
    pytest.param(
        dict(name='is-empty'),
        {'@name': 'is-empty', f'{NS}none': {}},
        id='empty'
    ),
])
def test_write_content(create_args: dict, expected: dict):
    bundle = ConfigBundle()
    bundle.create(options=[Option(bundle).create(**create_args)])
    assert xml_to_dict(bundle._to_xml(BundleConstructionArguments()), f'{NS}config', f'{NS}options', f'{NS}option') == expected


def test_write_long_content():
    content = b'*'*(ContentBasicElement.MAX_VALUE_LENGTH + 1)

    bundle = ConfigBundle()
    bundle.create(options=[
        Option(bundle).create(name='is-long-string', value=content)
    ])
    option = xml_to_dict(bundle._to_xml(BundleConstructionArguments()), f'{NS}config', f'{NS}options', f'{NS}option')
    assert set(option.keys()) == {'@name', '@encoding', '$'}
    assert decode_data(option['$'], option['@encoding']) == content
