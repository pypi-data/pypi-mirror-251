import os
from functools import wraps
from pathlib import Path
from unittest.mock import patch
from xml.etree.ElementTree import fromstring

import pytest
from xmljson import BadgerFish
from xsdata.models.enums import Namespace

from momotor.bundles import BundleFormatError, LxmlMissingError
# noinspection PyProtectedMember
from momotor.bundles.base import SCHEMA_NAMESPACE_LOCATION
from momotor.bundles.binding.momotor_1_0 import __NAMESPACE__
from momotor.bundles.utils.lxml import detect_lxml

NS = f'{{{__NAMESPACE__}}}'
XSI_NS = f'{{{Namespace.XS.uri}}}'
XML_NS = f'{{{Namespace.XML.uri}}}'
NS_LOCATION = __NAMESPACE__ + ' ' + SCHEMA_NAMESPACE_LOCATION


mark_skipif_no_lxml = pytest.mark.skipif(
    not detect_lxml(),
    reason="No lxml support"
)

mark_xfail_sax = pytest.mark.xfail(
    raises=BundleFormatError,
    reason="SAX parser does not support xsl stylesheets"
)

mark_xfail_no_lxml = pytest.mark.xfail(
    raises=LxmlMissingError,
    reason="To use lxml, install the momotor-bundles package with the lxml option: momotor-bundles[lxml]"
)


def parametrize_use_lxml(f):
    return pytest.mark.parametrize(
        "use_lxml",
        [
            pytest.param(True, id='use lxml', marks=mark_skipif_no_lxml),
            pytest.param(False, id='do not use lxml')
        ]
    )(f)


def parametrize_lxml(f):
    @wraps(f)
    def wrapped(has_lxml, *args, **kwargs):
        with patch('momotor.bundles.utils.lxml.has_lxml', new=has_lxml):
            return f(*args, has_lxml=has_lxml, **kwargs)

    return pytest.mark.parametrize(
        ("use_lxml", "has_lxml"),
        [
            pytest.param(True, True, id='use lxml, has lxml', marks=mark_skipif_no_lxml),
            pytest.param(True, False, id='use lxml, does not have lxml', marks=mark_xfail_no_lxml),
            pytest.param(False, True, id='do not use lxml, has lxml', marks=mark_skipif_no_lxml),
            pytest.param(False, False, id='do not use lxml, does not have lxml'),
            pytest.param(None, True, id='auto lxml, has lxml', marks=mark_skipif_no_lxml),
            pytest.param(None, False, id='auto lxml, does not have lxml'),
        ]
    )(wrapped)


bf = BadgerFish(dict_type=dict)


def xml_to_dict(xml: bytes, *path) -> dict:
    result = bf.data(fromstring(xml))
    for p in path:
        result = result[p]
    return result


def listfiles(path: Path):
    for root, dirs, files in os.walk(path):
        root = Path(root)
        for f in files:
            yield str(root.relative_to(path) / f), (root / f).read_text()


def listfilenames(path: Path):
    for root, dirs, files in os.walk(path):
        root = Path(root)
        for f in files:
            fp = root.relative_to(path) / f
            if not fp.is_dir():
                yield str(fp)


def datahash(data: bytes) -> str:
    import hashlib
    return hashlib.sha256(data).hexdigest()


def filehash(path: Path) -> str:
    return datahash(path.read_bytes())
