import re

from momotor.bundles.utils.rglob import rglob, filter, translate


PATHS1 = ['hello/world.py', 'hello/world.pyc',
          'hello/world/other/folder/example.py']

PATHS2 = ['example/l1/l2/test3-1.py', 'example/l1/test2-1.py',
          'example/l1/test2-2.py', 'example/l1/l2/l3/test4-1.py',
          'example/test1-1.py']


def test_rglob():
    assert rglob('hello/world.py', 'hello/*')
    assert rglob('hello/world.py', 'hello/*.py')
    assert rglob('hello/world.py', '**')
    assert rglob('hello/world.py', '**.py')
    assert rglob('hello/world.py', 'hello/**')
    assert rglob('hello/world.py', 'hello/**.py')
    assert not rglob('hello/other/world.py', 'hello/*')
    assert not rglob('hello/other/world.py', 'hello/*.py')
    assert rglob('hello/other/world.py', '**')
    assert rglob('hello/other/world.py', '**.py')
    assert rglob('hello/other/world.py', 'hello/**')
    assert rglob('hello/other/world.py', 'hello/**.py')
    assert rglob('world.py', '**/world.py')
    assert rglob('hello/world.py', '**/world.py')
    assert rglob('hello/other/world.py', '**/world.py')


def test_filter():
    assert filter(PATHS1, 'hello/*') == PATHS1[0:2]
    assert filter(PATHS1, 'hello/*.py') == PATHS1[0:1]
    assert filter(PATHS1, 'hello/**') == PATHS1
    assert filter(PATHS1, 'hello/**.py') == PATHS1[0:3:2]


def test_translate():
    regex = translate('example/**')
    assert regex == '(?ms)example/.*?$'
    assert re.findall(regex, '\n'.join(PATHS2)) == PATHS2

    regex = translate('example/**/*.py')
    assert regex == '(?ms)example/(?:.*?[\\\\/])?[^\\\\/]*\\.py$'
    assert re.findall(regex, '\n'.join(PATHS2)) == PATHS2

    regex = translate('example/*/*.py')
    assert regex == '(?ms)example/[^\\\\/]*/[^\\\\/]*\\.py$'
    assert re.findall(regex, '\n'.join(PATHS2)) == PATHS2[1:3]

    regex = translate('hello/world.?')
    assert regex == '(?ms)hello/world\\.[^\\\\/]$'
    assert re.findall(regex, '\n'.join(PATHS1)) == []

    regex = translate('hello/world.???')
    assert regex == '(?ms)hello/world\\.[^\\\\/]{3}$'
    assert re.findall(regex, '\n'.join(PATHS1)) == PATHS1[1:2]
