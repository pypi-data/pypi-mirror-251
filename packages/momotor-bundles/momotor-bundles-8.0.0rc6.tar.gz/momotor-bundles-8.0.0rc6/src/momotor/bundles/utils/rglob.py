"""Filename matching with shell patterns.

rglob(FILENAME, PATTERN) matches according to the local convention.
rglobcase(FILENAME, PATTERN) always takes case in account.

The functions operate by translating the pattern into a regular
expression.  They cache the compiled regular expressions for speed.

The function translate(PATTERN) returns a regular expression
corresponding to PATTERN.  (It does not compile it.)

---

Cloned from pywildcard <https://pypi.org/project/pywildcard/>,
modified to match behaviour of :py:func:`glob.glob` with `recursive=True`:

* ``**/`` and ``**\\`` match zero or more directories, instead of requiring at least a path separator to match
* `?` matches any character except the path separator, instead of matching any character
* Fix incorrect matching on non-posix systems by properly escaping ``\\`` in the generated regular expression

"""

import re

__all__ = ["filter", "rglob", "rglobcase", "translate"]

_cache = {}
_MAXCACHE = 100


def _purge():
    """Clear the pattern cache."""
    _cache.clear()


def rglob(name, pat):
    """Test whether FILENAME matches PATTERN.

    Patterns are Unix shell style:

    **      matches everything
    *       matches in one level
    ?       matches any single character
    [seq]   matches any character in seq
    [!seq]  matches any char not in seq

    An initial period in FILENAME is not special.
    Both FILENAME and PATTERN are first case-normalized
    if the operating system requires it.
    If you don't want this, use fnmatchcase(FILENAME, PATTERN).
    """
    import os
    name = os.path.normcase(name)
    pat = os.path.normcase(pat)
    return rglobcase(name, pat)


def filter(names, pat):
    """Return the subset of the list NAMES that match PAT."""
    import os
    import posixpath
    result = []
    pat = os.path.normcase(pat)
    try:
        re_pat = _cache[pat]
    except KeyError:
        res = translate(pat)
        if len(_cache) >= _MAXCACHE:
            _cache.clear()
        _cache[pat] = re_pat = re.compile(res)
    match = re_pat.match
    if os.path is posixpath:
        # normcase on posix is NOP. Optimize it away from the loop.
        for name in names:
            if match(name):
                result.append(name)
    else:
        for name in names:
            nc = os.path.normcase(name)
            if match(nc):
                result.append(name)
    return result


def rglobcase(name, pat):
    """Test whether FILENAME matches PATTERN, including case.

    This is a version of fnmatch() which doesn't case-normalize
    its arguments.
    """
    try:
        re_pat = _cache[pat]
    except KeyError:
        res = translate(pat)
        if len(_cache) >= _MAXCACHE:
            _cache.clear()
        _cache[pat] = re_pat = re.compile(res)
    return re_pat.match(name) is not None


def translate(pat):
    """Translate a shell PATTERN to a regular expression.

    There is no way to quote meta-characters.
    """
    i, n = 0, len(pat)
    res, c = '', ''
    while i < n:
        c = pat[i]
        i = i + 1

        count = 1
        if c in {'*', '?'}:
            while i < n and pat[i] == c:
                count += 1
                i += 1

        if c == '*':
            if count == 1:
                # "*"
                res = res + r'[^\\/]*'

            elif i < n and pat[i] in {'/', '\\'}:
                # "**/" or "**\"
                res = res + r'(?:.*?[\\/])?'
                i = i + 1

            else:
                # "**"
                res = res + r'.*?'

        elif c == '?':
            res = res + r'[^\\/]'
            if count > 1:
                res = res + '{%d}' % count

        elif c == '[':
            j = i
            if j < n and pat[j] == '!':
                j = j + 1
            if j < n and pat[j] == ']':
                j = j + 1
            while j < n and pat[j] != ']':
                j = j + 1
            if j >= n:
                res = res + r'\\['
            else:
                stuff = pat[i:j].replace('\\', '\\\\')
                i = j + 1
                if stuff[0] == '!':
                    stuff = '^' + stuff[1:]
                elif stuff[0] == '^':
                    stuff = r'\\' + stuff
                res = '%s[%s]' % (res, stuff)

        else:
            res = res + re.escape(c)

    return '(?ms)' + res + '$'
