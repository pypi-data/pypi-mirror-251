import pytest

from momotor.bundles.utils.keyedtuple import KeyedTuple


class Id:
    def __init__(self, id):
        self.id = id


class Name:
    def __init__(self, name):
        self.name = name


id_a = Id('a')
id_a_alt = Id('a')
id_b = Id('b')
id_c = Id('c')
id_d = Id('d')
id_abc = [id_a, id_b, id_c]

name_a = Name('a')
name_e = Name('e')


def test_keyedtuple_getitem():
    idl = KeyedTuple(id_abc)

    # by index
    assert idl[0] == id_a
    assert idl[1] == id_b
    assert idl[2] == id_c
    with pytest.raises(IndexError):
        _ = idl[3]

    # by key
    assert idl['a'] == id_a
    assert idl['b'] == id_b
    assert idl['c'] == id_c
    with pytest.raises(KeyError):
        _ = idl['d']

    # by item
    assert idl[id_a] == id_a
    assert idl[id_b] == id_b
    assert idl[id_c] == id_c

    with pytest.raises(KeyError):
        _ = idl[id_d]

    with pytest.raises(KeyError):
        _ = idl[id_a_alt]

    with pytest.raises(ValueError):
        # noinspection PyTypeChecker
        _ = idl[name_a]

    # slicing is not supported
    with pytest.raises(IndexError):
        _ = idl[1:2]


def test_keylist_contains():
    idl = KeyedTuple(id_abc)

    # by index
    assert 0 in idl
    assert 1 in idl
    assert 2 in idl
    assert 3 not in idl

    # by key
    assert 'a' in idl
    assert 'b' in idl
    assert 'c' in idl
    assert 'd' not in idl

    # by item
    assert id_a in idl
    assert id_b in idl
    assert id_c in idl
    assert id_d not in idl
    assert id_a_alt not in idl
    assert name_a not in idl
    assert name_e not in idl


def test_keyedtuple_get_unknown_item_with_known_id():
    idl = KeyedTuple(id_abc)
    id_a2 = Id('a')

    with pytest.raises(KeyError):
        _ = idl[id_a2]


def test_keyedtuple_get():
    idl = KeyedTuple(id_abc)

    assert idl.get('a') == id_a
    assert idl.get('d') is None

    _placeholder = object()
    # noinspection PyTypeChecker
    assert idl.get('d', _placeholder) == _placeholder


def test_keyedtuple_from_dict():
    idl = KeyedTuple({'a': id_a})
    assert list(idl.keys()) == ['a']


def test_keyedtuple_from_invalid_dict():
    with pytest.raises(KeyError):
        _ = KeyedTuple({'*': id_a})


def test_keyedtuple_iter():
    idl = KeyedTuple(id_abc)

    keys = []
    for item in idl:
        keys.append(item.id)

    assert keys == ['a', 'b', 'c']


def test_keyedtuple_copy():
    idl1 = KeyedTuple(id_abc)
    idl2 = idl1.copy()
    assert id(idl1) != id(idl2)


def test_keyedtuple_len():
    idl0 = KeyedTuple()
    assert len(idl0) == 0

    idl1 = KeyedTuple([id_a])
    assert len(idl1) == 1


def test_keyedtuple_eq():
    idl0 = KeyedTuple()
    idl0a = KeyedTuple()
    idl0_not_id = KeyedTuple(key_attr='not_id')
    idl1 = KeyedTuple([id_a])
    idl1a = KeyedTuple([id_a])

    assert idl0 == idl0a
    assert idl0 != idl1
    assert idl0 != idl0_not_id
    assert idl1 == idl1a
    assert idl1 == [id_a]
    assert idl1 == {'a': id_a}


def test_keyedtuple_count():
    idl1 = KeyedTuple(id_abc)

    assert idl1.count(id_a) == 1
    assert idl1.count(id_d) == 0
    assert idl1.count(id_a_alt) == 0
    assert idl1.count(name_a) == 0
