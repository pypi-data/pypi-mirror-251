import pytest

from momotor.bundles.utils.filters import Any, All, Not, F, FilterableList


def _get_test_list() -> FilterableList:
    fl = FilterableList()
    
    class A(object):
        def __init__(self, alpha):
            self.alpha = alpha
            
        def __str__(self):
            return f'A({self.alpha})'
    
    class B(object):
        def __init__(self, beta):
            self.beta = beta
    
        def __str__(self):
            return f'B({self.beta})'
    
    class AB(object):
        def __init__(self, alpha, beta):
            self.alpha = alpha
            self.beta = beta
            
        def __str__(self):
            return f'AB({self.alpha},{self.beta})'

    fl.append(A('alpha'))
    fl.append(A(['alpha', 'beta']))
    fl.append(B('beta'))
    fl.append(AB('alpha', 'beta'))
    fl.append(AB('Alpha', 'Beta'))
    fl.append(AB('beta', 'alpha'))

    return fl


test_list = _get_test_list()


def _iter_to_str(it):
    return ','.join(map(str, it))


def make_test(*args, expected, **kwargs):
    label = _iter_to_str(args) + ','.join(f'{k}={v!r}' for k, v in kwargs.items())
    if not label:
        label = 'empty'

    return pytest.param(args, kwargs, expected, id=label)


@pytest.mark.parametrize([
    'query_args', 'query_kwargs', 'expected'
], [
    # equal
    make_test(alpha='alpha', expected='A(alpha),AB(alpha,beta)'),
    make_test(alpha=['alpha', 'beta'], expected="A(['alpha', 'beta'])"),
    make_test(beta='beta', expected='B(beta),AB(alpha,beta)'),
    make_test(alpha='gamma', expected=''),
    make_test(gamma='gamma', expected=''),
    make_test(alpha__is='alpha', expected='A(alpha),AB(alpha,beta)'),
    make_test(alpha__eq='alpha', expected='A(alpha),AB(alpha,beta)'),

    # iequal
    make_test(alpha__ieq='alpha', expected='A(alpha),AB(alpha,beta),AB(Alpha,Beta)'),
    make_test(alpha__ieq=['ALPHA', 'beta'], expected="A(['alpha', 'beta'])"),
    make_test(beta__ieq='beta', expected='B(beta),AB(alpha,beta),AB(Alpha,Beta)'),

    # not-equal
    make_test(alpha__ne='alpha', expected="A(['alpha', 'beta']),AB(Alpha,Beta),AB(beta,alpha)"),
    make_test(beta__ne='beta', expected='AB(Alpha,Beta),AB(beta,alpha)'),
    make_test(alpha__ne='gamma', expected="A(alpha),A(['alpha', 'beta']),AB(alpha,beta),AB(Alpha,Beta),AB(beta,alpha)"),
    make_test(gamma__ne='gamma', expected=''),

    # not-iequal
    make_test(alpha__ine='alpha', expected="A(['alpha', 'beta']),AB(beta,alpha)"),
    make_test(beta__ine='beta', expected='AB(beta,alpha)'),

    # contains
    make_test(alpha__contains='a', expected='A(alpha),AB(alpha,beta),AB(Alpha,Beta),AB(beta,alpha)'),
    make_test(alpha__contains='A', expected='AB(Alpha,Beta)'),
    make_test(alpha__contains='x', expected=''),
    make_test(beta__contains='b', expected='B(beta),AB(alpha,beta)'),

    # icontains
    make_test(beta__icontains='b', expected='B(beta),AB(alpha,beta),AB(Alpha,Beta)'),

    # in
    make_test(alpha__in=['alpha', 'beta'], expected='A(alpha),AB(alpha,beta),AB(beta,alpha)'),

    # iin
    make_test(alpha__iin=['alpha', 'beta'], expected='A(alpha),AB(alpha,beta),AB(Alpha,Beta),AB(beta,alpha)'),

    # startswith
    make_test(alpha__startswith='a', expected='A(alpha),AB(alpha,beta)'),

    # istartswith
    make_test(alpha__istartswith='a', expected='A(alpha),AB(alpha,beta),AB(Alpha,Beta)'),

    # endswith
    make_test(alpha__endswith='a', expected='A(alpha),AB(alpha,beta),AB(Alpha,Beta),AB(beta,alpha)'),
    make_test(alpha__endswith='A', expected=''),
    make_test(alpha__endswith='b', expected=''),

    # iendswith
    make_test(alpha__iendswith='A', expected='A(alpha),AB(alpha,beta),AB(Alpha,Beta),AB(beta,alpha)'),

    # glob
    make_test(alpha__glob='*et*', expected='AB(beta,alpha)'),
    make_test(alpha__glob='"*et*" "*lp*"', expected='A(alpha),AB(alpha,beta),AB(Alpha,Beta),AB(beta,alpha)'),
    make_test(beta__glob='*et*', expected='B(beta),AB(alpha,beta),AB(Alpha,Beta)'),
    make_test(alpha__glob='Alp*', expected='AB(Alpha,Beta)'),

    # iglob
    make_test(alpha__iglob='Alp*', expected='A(alpha),AB(alpha,beta),AB(Alpha,Beta)'),

    # re
    make_test(alpha__re='et', expected='AB(beta,alpha)'),
    make_test(alpha__re='^et', expected=''),
    make_test(alpha__re='^bet', expected='AB(beta,alpha)'),
    make_test(alpha__re='^bet$', expected=''),
    make_test(alpha__re='E', expected=''),

    # ire
    make_test(alpha__ire='E', expected='AB(beta,alpha)'),

    # empty
    make_test(expected="A(alpha),A(['alpha', 'beta']),B(beta),AB(alpha,beta),AB(Alpha,Beta),AB(beta,alpha)"),

    # Not()
    make_test(Not(alpha='alpha'), expected="A(['alpha', 'beta']),B(beta),AB(Alpha,Beta),AB(beta,alpha)"),
    make_test(Not(beta='beta'), expected="A(alpha),A(['alpha', 'beta']),AB(Alpha,Beta),AB(beta,alpha)"),
    make_test(Not(alpha='gamma'), expected="A(alpha),A(['alpha', 'beta']),B(beta),AB(alpha,beta),AB(Alpha,Beta),AB(beta,alpha)"),
    make_test(Not(gamma='gamma'), expected="A(alpha),A(['alpha', 'beta']),B(beta),AB(alpha,beta),AB(Alpha,Beta),AB(beta,alpha)"),

    # All
    make_test(All(F(alpha='alpha'), F(alpha='beta')), expected=''),
    make_test(All(alpha='alpha', beta='beta'), expected='AB(alpha,beta)'),

    # ~All
    make_test(~All(alpha='alpha'), expected="A(['alpha', 'beta']),B(beta),AB(Alpha,Beta),AB(beta,alpha)"),

    # Any
    make_test(Any(F(alpha='alpha'), F(alpha='beta')), expected='A(alpha),AB(alpha,beta),AB(beta,alpha)'),
    make_test(Any(alpha='alpha', beta='beta'), expected='A(alpha),B(beta),AB(alpha,beta)'),

    # ~Any
    make_test(~Any(alpha='alpha', beta='beta'), expected="A(['alpha', 'beta']),AB(Alpha,Beta),AB(beta,alpha)"),

    # Multiple
    make_test(All(alpha='alpha'), All(beta='beta'), expected='AB(alpha,beta)'),
    make_test(All(F(alpha='alpha'), F(beta='beta')), expected='AB(alpha,beta)'),
    make_test(All(F(alpha__glob='al*'), F(beta__glob='be*')), expected='AB(alpha,beta)'),
    make_test(All(alpha='alpha'), beta='beta', expected='AB(alpha,beta)'),
    make_test(alpha='alpha', beta='beta', expected='AB(alpha,beta)'),
    make_test(All(alpha='alpha'), All(alpha='beta'), expected=''),
    make_test(All(alpha__re='a'), All(alpha__re='t'), expected='AB(beta,alpha)'),
])
def test_filter(query_args, query_kwargs, expected):
    assert _iter_to_str(
        test_list.filter(*query_args, **query_kwargs)
    ) == expected


@pytest.mark.parametrize([
    'query_args', 'query_kwargs', 'expected'
], [
    make_test(alpha='alpha', expected="A(['alpha', 'beta']),B(beta),AB(Alpha,Beta),AB(beta,alpha)"),
])
def test_exclude(query_args, query_kwargs, expected):
    assert _iter_to_str(
        test_list.exclude(*query_args, **query_kwargs)
    ) == expected


@pytest.mark.parametrize([
    'first_kwargs', 'second_kwargs', 'expected'
], [
    pytest.param(dict(alpha='alpha'), dict(beta='beta'), 'AB(alpha,beta)'),
])
def test_chain_filter_filter(first_kwargs, second_kwargs, expected):
    assert _iter_to_str(
        test_list.filter(**first_kwargs).filter(**second_kwargs)
    ) == expected


@pytest.mark.parametrize([
    'first_kwargs', 'second_kwargs', 'expected'
], [
    pytest.param(dict(alpha='alpha'), dict(beta='beta'), 'A(alpha)'),
])
def test_chain_filter_exclude(first_kwargs, second_kwargs, expected):
    assert _iter_to_str(
        test_list.filter(**first_kwargs).exclude(**second_kwargs)
    ) == expected
