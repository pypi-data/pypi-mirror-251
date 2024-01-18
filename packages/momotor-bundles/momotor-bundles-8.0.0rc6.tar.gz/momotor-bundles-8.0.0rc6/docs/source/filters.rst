.. _filters:

==================
Sequence filtering
==================

The :py:mod:`momotor.bundles.utils.filters` package provides two filterable sequences, the
:py:class:`~momotor.bundles.utils.filters.FilterableList` and
:py:class:`~momotor.bundles.utils.filters.FilterableTuple`.
Both add the same functions to the standard python :py:class:`list` and :py:class:`tuple` types.

The interface is loosely based on Django QuerySets field lookups.

.. comment

    >>> import typing
    >>> from momotor.bundles.utils.filters import *
    >>> from dataclasses import dataclass, field
    >>> @dataclass
    ... class ItemA:
    ...    a: typing.Any = field()
    >>> @dataclass
    ... class ItemAB:
    ...    a: typing.Any = field()
    ...    b: typing.Any = field()

The examples in this documentation use the following filterable lists:

    >>> data_str = FilterableList([ItemA(a='abc'), ItemA(a='ABC'), ItemA(a='def'), ItemA(a='abc/def')])
    >>> data_int = FilterableList([ItemA(a=1), ItemA(a=2), ItemA(a=3)])
    >>> data_set = FilterableList([ItemA(a={1, 2}), ItemA(a={2, 3}), ItemA(a={3, 4})])
    >>> data_ab = FilterableList([ItemAB(a=1, b=1), ItemAB(a=1, b=2), ItemAB(a=2, b=2), ItemAB(a=3, b=3)])

Where `ItemA` and `ItemAB` are datatypes having both an `a` attribute, and `ItemAB` also has a `b` attribute.

.. _filtering and excluding:

-----------------------
Filtering and excluding
-----------------------

The most basic lookup looks like this:

    >>> data_ab.filter(a=1)  # filter all items with a==1
    [ItemAB(a=1, b=1), ItemAB(a=1, b=2)]

This filters `data_ab` for any objects containing an `a` attribute with value equal to ``1``.

The result of :py:meth:`~momotor.bundles.utils.filters.FilterableList.filter` is itself another filterable type,
so filters can be chained:

    >>> data_ab.filter(a=1).filter(b=2)  # filter all items with a==1, the filter the result for a==2
    [ItemAB(a=1, b=2)]

``FilterableList.exclude(...)`` excludes items:

    >>> data_ab.exclude(a=1)  # exclude all items where a==1
    [ItemAB(a=2, b=2), ItemAB(a=3, b=3)]

Providing multiple lookups in ``filter()`` or ``exclude()`` will filter or exclude objects matching all the lookups:

    >>> data_ab.filter(a=1, b=2)  # filter all items with a==1 and b==2
    [ItemAB(a=1, b=2)]

    >>> data_ab.exclude(a=1, b=2)  # exclude all items with a==1 and b==2
    [ItemAB(a=1, b=1), ItemAB(a=2, b=2), ItemAB(a=3, b=3)]

.. _not object:

Not() object
------------

Lookups can be negated using a :py:class:`~momotor.bundles.utils.filters.Not` object:

    >>> data_ab.filter(Not(a=1))  # filter all items where `a` is not 1
    [ItemAB(a=2, b=2), ItemAB(a=3, b=3)]

``FilterableList.exclude(...)`` is a shortcut for ``FilterableList.filter(Not(...))``

.. _all object:

All() object
------------

The :py:class:`~momotor.bundles.utils.filters.All` object can be used to make lookups with multiple arguments
more explicit:

    >>> data_ab.filter(All(a=1, b=2))  # filter all items with a==1 and b==2
    [ItemAB(a=1, b=2)]

.. _any object:

Any() object
------------

Lookups can also be combined using the :py:class:`~momotor.bundles.utils.filters.Any` object to find an object
which matches *any* of the requested lookups:

    >>> data_ab.filter(Any(a=1, b=2))  # filter all items with a==1 OR b==2
    [ItemAB(a=1, b=1), ItemAB(a=1, b=2), ItemAB(a=2, b=2)]

.. _f object:

Combining filter objects
------------------------

Lookup objects can be combined, for example:

    >>> data_ab.filter(Any(All(a=1, b=2), b=3))  # Look for items with (a==1 AND b==2) OR b==3
    [ItemAB(a=1, b=2), ItemAB(a=3, b=3)]

F() object
----------

Using keyword arguments it is not possible to filter for multiple values of the same property, since
``filter(a=1, a=3)`` has a repeated keyword ``a``:

.. doctest-skip::

    >>> data_ab.filter(a=1, a=3)  # this is a SyntaxError
    Traceback (most recent call last):
    ...
    SyntaxError: keyword argument repeated

To look for ``data_ab`` values for the same attribute, use the :py:class:`~momotor.bundles.utils.filters.F` object
to wrap individual queries:

    >>> data_ab.filter(F(a=1), F(a=3))  # filter all items with a==1 AND a==3 (which is nonsensical indeed, but this is just an example)
    []

This can also be combined with the other filter objects like :py:class:`~momotor.bundles.utils.filters.Any`

    >>> data_ab.filter(Any(F(a=1), F(a=3)))  # filter items with a==1 OR a==3
    [ItemAB(a=1, b=1), ItemAB(a=1, b=2), ItemAB(a=3, b=3)]

:py:class:`~momotor.bundles.utils.filters.F` objects can also be used to easily pass on filter queries as
arguments to functions:

    >>> def filter_data(f: F):
    ...     return data_ab.filter(f)

    >>> for f in [F(a=1), F(a=2)]:
    ...     print(filter_data(f))
    [ItemAB(a=1, b=1), ItemAB(a=1, b=2)]
    [ItemAB(a=2, b=2)]

:py:class:`~momotor.bundles.utils.filters.Any`, :py:class:`~momotor.bundles.utils.filters.All` and
:py:class:`~momotor.bundles.utils.filters.Not` are subclasses of :py:class:`~momotor.bundles.utils.filters.F`.

When mixing :py:class:`~momotor.bundles.utils.filters.F` arguments and keyword arguments, Python syntax requires
the positional arguments to be provided before the keyword arguments. The following is invalid:

.. doctest-skip::

    >>> data_ab.filter(a=1, Any(a=2, b=3))  # positional argument follows keyword argument
    Traceback (most recent call last):
    ...
    SyntaxError: positional argument follows keyword argument

Using an :py:class:`~momotor.bundles.utils.filters.F` object solves this issue:

    >>> data_ab.filter(F(a=1), Any(a=2, b=3))
    []

Negation
--------

The :py:class:`~momotor.bundles.utils.filters.Any` and :py:class:`~momotor.bundles.utils.filters.All` classes
support negation using the `~` operator, for example `~All(...)` is the same as `Not(All(...))`

------------
Lookup types
------------

Additionally to filtering or excluding exact values, there are several other lookup types.
A lookup type is added to the lookup by separating the attribute name and the lookup with a double underscore
``__``, eg. ``a__ne`` applies the :py:ref:`not-equal lookup <ne lookup>` to the `a` attribute.

The following filter lookup operations are available:

+-----------------------------+-------------------------------------------+-------------------------------------------+
| Lookup type                 | Case sensitive lookup                     | Case insensitive lookup                   |
+=============================+===========================================+===========================================+
| Is-equal                    | :ref:`(none) / eq / is <eq lookup>`       | :ref:`ieq / iis <ieq lookup>`             |
+-----------------------------+-------------------------------------------+-------------------------------------------+
| Not-equal                   | :ref:`ne <ne lookup>`                     | :ref:`ine <ine lookup>`                   |
+-----------------------------+-------------------------------------------+-------------------------------------------+
| Contains                    | :ref:`contains <contains lookup>`         | :ref:`icontains <icontains lookup>`       |
+-----------------------------+-------------------------------------------+-------------------------------------------+
| In                          | :ref:`in <in lookup>`                     | :ref:`iin <iin lookup>`                   |
+-----------------------------+-------------------------------------------+-------------------------------------------+
| Starts-with                 | :ref:`startswith <startswith lookup>`     | :ref:`istartswith <istartswith lookup>`   |
+-----------------------------+-------------------------------------------+-------------------------------------------+
| Ends-with                   | :ref:`endswith <endswith lookup>`         | :ref:`iendswith <iendswith lookup>`       |
+-----------------------------+-------------------------------------------+-------------------------------------------+
| Glob                        | :ref:`glob <glob lookup>`                 | :ref:`iglob <iglob lookup>`               |
+-----------------------------+-------------------------------------------+-------------------------------------------+
| Recursive glob              | :ref:`rglob <rglob lookup>`               | :ref:`irglob <irglob lookup>`             |
+-----------------------------+-------------------------------------------+-------------------------------------------+
| Regular expression          | :ref:`re <re lookup>`                     | :ref:`ire <ire lookup>`                   |
+-----------------------------+-------------------------------------------+-------------------------------------------+

.. note::
    Case insensitive lookups only accept strings or a sequence of strings. Any other value
    will raise a :py:exc:`TypeError`:

        >>> data_int.filter(a__ine=1)
        Traceback (most recent call last):
        ...
        TypeError: Expected a string or sequence of strings, got <class 'int'>


.. _eq lookup:

Is-equal lookup
---------------

Filters exact values.

Operator: No operator, ``is`` or ``eq``

Examples:

    >>> data_str.filter(a='abc')
    [ItemA(a='abc')]

    >>> data_str.filter(a__is='ABC')
    [ItemA(a='ABC')]

    >>> data_str.filter(a__eq='def')
    [ItemA(a='def')]

    >>> data_int.filter(a=1)
    [ItemA(a=1)]

    >>> data_int.filter(a='abc')
    []

.. _ieq lookup:

Is-equal lookup (case insensitive)
----------------------------------

Filters string attributes case insensitive.

Lookup operator: ``ieq`` / ``iis``

Examples:

    >>> data_str.filter(a__ieq='abc')
    [ItemA(a='abc'), ItemA(a='ABC')]

    >>> data_int.filter(a__iis='abc')
    []

.. _ne lookup:

Not-equal lookup
----------------

Lookup operator: ``ne``

Usage example:

    >>> data_str.filter(a__ne='abc')
    [ItemA(a='ABC'), ItemA(a='def'), ItemA(a='abc/def')]

    >>> data_int.filter(a__ne=1)
    [ItemA(a=2), ItemA(a=3)]

.. _ine lookup:

Not-equal lookup (case insensitive)
-----------------------------------

Lookup operator: ``ine``

Usage example:

    >>> data_str.filter(a__ine='abc')
    [ItemA(a='def'), ItemA(a='abc/def')]

.. _contains lookup:

Contains lookup
---------------

Lookup operator: ``contains``

Works on Python types implementing :py:meth:`object.__contains__` like :py:class:`str`, sequences and sets.

Usage example:

    >>> data_str.filter(a__contains='a')
    [ItemA(a='abc'), ItemA(a='abc/def')]

    >>> data_set.filter(a__contains=2)
    [ItemA(a={1, 2}), ItemA(a={2, 3})]

.. _icontains lookup:

Contains lookup (case insensitive)
----------------------------------

Lookup operator: ``icontains``

Works on Python :py:class:`str` and sets and sequences containing strings.

Usage example:

    >>> data_str.filter(a__icontains='a')
    [ItemA(a='abc'), ItemA(a='ABC'), ItemA(a='abc/def')]

.. _in lookup:

In lookup
---------

Lookup operator: ``in``

The reverse of :py:ref:`contains <contains lookup>`. The lookup value must implement :py:meth:`object.__contains__`

Usage example:

    >>> data_str.filter(a__in={'abc', 'def', 'ghi'})
    [ItemA(a='abc'), ItemA(a='def')]

    >>> data_int.filter(a__in={0, 1, 2})
    [ItemA(a=1), ItemA(a=2)]

.. _iin lookup:

In lookup (case insensitive)
----------------------------

Lookup operator: ``iin``

Usage example:

    >>> data_str.filter(a__iin={'abc', 'def', 'ghi'})
    [ItemA(a='abc'), ItemA(a='ABC'), ItemA(a='def')]

.. _startswith lookup:

Starts-with lookup
------------------

Lookup operator: ``startswith``

Usage example:

    >>> data_str.filter(a__startswith='a')
    [ItemA(a='abc'), ItemA(a='abc/def')]

.. _istartswith lookup:

Starts-with lookup (case insensitive)
-------------------------------------

Lookup operator: ``istartswith``

Usage example:

    >>> data_str.filter(a__istartswith='a')
    [ItemA(a='abc'), ItemA(a='ABC'), ItemA(a='abc/def')]

.. _endswith lookup:

Ends-with lookup
----------------

Lookup operator: ``endswith``

Usage example:

    >>> data_str.filter(a__endswith='c')
    [ItemA(a='abc')]

.. _iendswith lookup:

Ends-with lookup (case insensitive)
-----------------------------------

Lookup operator: ``iendswith``

Usage example:

    >>> data_str.filter(a__iendswith='c')
    [ItemA(a='abc'), ItemA(a='ABC')]

.. _glob lookup:

Glob lookup
-----------

Lookup operator: ``glob``

Matches a string against a pattern. The pattern is a string with special characters:

* ``*`` matches any number of characters
* ``?`` matches any single character
* ``[seq]`` matches any character in seq
* ``[!seq]`` matches any character not in seq

Unlike the :ref:`rglob <rglob lookup>` filter, path separators characters (``/`` and ``\``) are not considered
special and are matched by the ``*`` pattern.

Usage example:

    >>> data_str.filter(a__glob='a*')
    [ItemA(a='abc'), ItemA(a='abc/def')]

.. _iglob lookup:

Glob lookup (case insensitive)
------------------------------

Lookup operator: ``iglob``

Matches a string against a pattern, case insensitive.
The pattern is a string with special characters:

* ``*`` matches any number of characters
* ``?`` matches any single character
* ``[seq]`` matches any character in seq
* ``[!seq]`` matches any character not in seq

Unlike the :ref:`irglob <irglob lookup>` filter, path separators characters (``/`` and ``\``) are not considered
special and are matched by the ``*`` pattern.

Usage example:

    >>> data_str.filter(a__iglob='a*')
    [ItemA(a='abc'), ItemA(a='ABC'), ItemA(a='abc/def')]

.. _rglob lookup:

Recursive glob lookup
---------------------

Lookup operator: ``rglob``

Matches a string against a recursive glob pattern. The pattern is a string with special characters:

* ``*`` matches any number of characters, excluding path separators
* ``**`` matches any number of characters, including path separators (except a trailing path separator, see below)
* ``?`` matches any single character
* ``[seq]`` matches any character in seq
* ``[!seq]`` matches any character not in seq

To match a string ending in a path separator (``/`` or ``\``, indicating a directory path), the pattern
must explicitly end in a path separator as well, i.e. ``**`` alone will *not* match strings ending with a path
separator, and ``**/`` or ``**\`` will *only* match strings ending with a path separator.

Usage example:

    >>> data_str.filter(a__rglob='a*')
    [ItemA(a='abc')]

    >>> data_str.filter(a__rglob='a**')
    [ItemA(a='abc'), ItemA(a='abc/def')]

.. _irglob lookup:

Recursive glob lookup (case insensitive)
----------------------------------------

Lookup operator: ``irglob``

Matches a string against a recursive glob pattern, case insensitive. The pattern is a string with special characters:

* ``*`` matches any number of characters, excluding path separators
* ``**`` matches any number of characters, including path separators (except a trailing path separator, see below)
* ``?`` matches any single character
* ``[seq]`` matches any character in seq
* ``[!seq]`` matches any character not in seq

To match a string ending in a path separator (``/``, indicating a directory path), the pattern
must explicitly end in a path separator as well, i.e. ``**`` alone will *not* match strings ending with a path
separator, and ``**/`` or ``**\`` will *only* match strings ending with a path separator.

Usage example:

    >>> data_str.filter(a__irglob='a*')
    [ItemA(a='abc'), ItemA(a='ABC')]

    >>> data_str.filter(a__irglob='a**')
    [ItemA(a='abc'), ItemA(a='ABC'), ItemA(a='abc/def')]

.. _re lookup:

Regular expression lookup
-------------------------

Lookup operator: ``re``

Usage example:

    >>> data_str.filter(a__re=r'^.b.$')
    [ItemA(a='abc')]

.. _ire lookup:

Regular expression lookup (case insensitive)
--------------------------------------------

Lookup operator: ``ire``

Usage example:

    >>> data_str.filter(a__ire=r'^.b.$')
    [ItemA(a='abc'), ItemA(a='ABC')]

------------------
Additional methods
------------------

:py:class:`~momotor.bundles.utils.filters.FilterableList` and
:py:class:`~momotor.bundles.utils.filters.FilterableTuple` have several more functions:

.. py:method:: ifilter(...)

   Same as :py:meth:`~momotor.bundles.utils.filters.FilterableList.filter`, but returning an iterable of items.

.. py:method:: iexclude(...)

   Same as :py:meth:`~momotor.bundles.utils.filters.FilterableList.exclude`, but returning an iterable of items.

.. py:method:: filter_with(func: Callable[[Any], bool])

   Filter the sequence using a filter function. The function receives an item and should return a boolean
   indicating if the item should be included in the result.
