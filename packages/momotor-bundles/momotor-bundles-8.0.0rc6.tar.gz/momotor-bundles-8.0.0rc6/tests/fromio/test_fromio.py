import contextlib
from pathlib import Path
from unittest.mock import patch

import pytest

from bundle_test_helpers import mark_skipif_no_lxml, mark_xfail_no_lxml, mark_xfail_sax, parametrize_lxml
from momotor.bundles import ProductBundle
from momotor.bundles.binding import ProductComplexType, FilesComplexType, FileComplexType
from momotor.bundles.binding.momotor_1_0 import __NAMESPACE__
from momotor.bundles.exception import BundleFormatError
from momotor.bundles.utils.arguments import BundleFactoryArguments


@pytest.mark.parametrize(
    ["filename", "use_lxml", "has_lxml"],
    [
        pytest.param('valid.xml', True, True, marks=mark_skipif_no_lxml),
        pytest.param('valid.xml', True, False, marks=mark_xfail_no_lxml),
        pytest.param('valid.xml', False, True, marks=mark_skipif_no_lxml),
        pytest.param('valid.xml', False, False),
        pytest.param('valid.xml', None, True, marks=mark_skipif_no_lxml),
        pytest.param('valid.xml', None, False),

        pytest.param('valid_xslt.xml', True, True, marks=mark_skipif_no_lxml),
        pytest.param('valid_xslt.xml', True, False, marks=mark_xfail_no_lxml),
        pytest.param('valid_xslt.xml', False, True, marks=[mark_xfail_sax, mark_skipif_no_lxml]),
        pytest.param('valid_xslt.xml', False, False, marks=mark_xfail_sax),
        pytest.param('valid_xslt.xml', None, True, marks=mark_skipif_no_lxml),
        pytest.param('valid_xslt.xml', None, False, marks=mark_xfail_sax),
    ]
)
def test_valid(filename, use_lxml, has_lxml):
    with patch('momotor.bundles.utils.lxml.has_lxml', new=has_lxml):
        args = BundleFactoryArguments(validate_signature=False)
        with contextlib.ExitStack() as stack:
            io = stack.enter_context((Path(__file__).parent / 'files' / filename).open('rb'))

            # noinspection PyProtectedMember
            instance, args = ProductBundle._from_io(io, stack, use_lxml=use_lxml, args=args)

            assert isinstance(instance, ProductComplexType)
            assert instance.id == 'product'

            assert 0 == len(instance.meta)
            assert 0 == len(instance.options)
            assert 1 == len(instance.files)

            files_node = instance.files[0]

            assert isinstance(files_node, FilesComplexType)
            assert 'files' == files_node.basesrc
            assert 1 == len(files_node.file)

            file_node = files_node.file[0]

            assert isinstance(file_node, FileComplexType)
            assert 'file_name' == file_node.name
            assert 'file_src' == file_node.src
            assert 'text/plain' == file_node.type_value


@parametrize_lxml
def test_invalid(has_lxml, use_lxml):
    if use_lxml or (use_lxml is None and has_lxml):
        match = (
            rf"Element '\{{{__NAMESPACE__}\}}option': "
            rf"This element is not expected\. Expected is \( \{{{__NAMESPACE__}\}}file \)\., line \d+"
        )
    else:
        match = rf'Unknown property \{{{__NAMESPACE__}\}}filesComplexType:\{{{__NAMESPACE__}\}}option'

    with pytest.raises(BundleFormatError, match=match), contextlib.ExitStack() as stack:
        path = Path(__file__).parent / 'files' / 'invalid.xml'
        args = BundleFactoryArguments(use_lxml=use_lxml, location_base=path.name, validate_signature=False)

        io = stack.enter_context(path.open('rb'))

        # noinspection PyProtectedMember
        ProductBundle._from_io(io, stack, args=args)
