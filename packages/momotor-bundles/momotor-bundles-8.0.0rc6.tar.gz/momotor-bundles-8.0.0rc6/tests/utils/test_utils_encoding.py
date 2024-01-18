from pathlib import PurePosixPath

import pytest

from momotor.bundles.utils.encoding import encode_posix_path


@pytest.mark.parametrize(["input", "output"], [
    [PurePosixPath(), PurePosixPath()],
    [PurePosixPath('test'), PurePosixPath('test')],
    [PurePosixPath('test', 'abc.def'), PurePosixPath('test', 'abc.def')],
    [PurePosixPath('test', 'abc..def'), PurePosixPath('test', 'abc..def')],
    [PurePosixPath('t\u2013st', 'abc.def'), PurePosixPath('tst-2n0a', 'abc.def')],
    [PurePosixPath('test', 'a\u2013bc.def'), PurePosixPath('test', 'abc-2n0a.def')],
    [PurePosixPath('test', 'abc.d\u2013ef'), PurePosixPath('test', 'abc.def-2n0a')],
    [PurePosixPath('test', 'a\u2013bc.d\u2013ef'), PurePosixPath('test', 'abc-2n0a.def-2n0a')],
])
def test_encode_path(input, output):
    assert encode_posix_path(input) == output
