from __future__ import annotations

import sys
from collections import deque
from collections.abc import Mapping, Set
from numbers import Number
from typing import Any, Collection, Dict, List, Optional

from .splitter import split

ZERO_DEPTH_BASES = (str, bytes, Number, range, bytearray)


def only_one(
    check: List[str],
    value: List[str],
    default: bool = True,
) -> Optional[str]:
    """Get only one element from check list that exists in match list.

    .. usage:
        >>> only_one(['a', 'b'], ['a', 'b', 'c'])
        'a'
        >>> only_one(['a', 'b'], ['c', 'e', 'f'])
        'c'
        >>> only_one(['a', 'b'], ['c', 'e', 'f'], default=False)

    """
    if len(exist := set(check).intersection(set(value))) == 1:
        return list(exist)[0]
    return next(
        (_ for _ in value if _ in check),
        (value[0] if default else None),
    )


def hasdot(search: str, content: Dict[Any, Any]) -> bool:
    """Return True value if dot searching exists in content data.

    .. usage:
        >>> hasdot('data.value', {'data': {'value': 2}})
        True
        >>> hasdot('data.value.key', {'data': {'value': 2}})
        False
        >>> hasdot('item.value.key', {'data': {'value': 2}})
        False
    """
    _search, _else = split(search, ".", maxsplit=1)
    if _search in content and isinstance(content, dict):
        if not _else:
            return True
        elif isinstance((result := content[_search]), dict):
            return hasdot(_else, result)
    return False


def getdot(
    search: str,
    content: Dict[Any, Any],
    *args,
    **kwargs,
) -> Any:
    """Return the value if dot searching exists in content data.

    .. usage:
        >>> getdot('data.value', {'data': {'value': 1}})
        1
        >>> getdot('data', {'data': 'test'})
        'test'
        >>> getdot('data.value', {'data': 'test'})
        Traceback (most recent call last):
        ...
        ValueError: 'value' does not exists in test
        >>> getdot('data.value', {'data': {'key': 1}}, None)

        >>> getdot(
        ...     'data.value.getter',
        ...     {'data': {'value': {'getter': 'success', 'put': 'fail'}}},
        ... )
        'success'
        >>> getdot('foo.bar', {"foo": {"baz": 1}}, ignore=True)

        >>> getdot('foo.bar', {"foo": {"baz": 1}}, 2, 3)
        2
        >>> getdot('foo.bar', {"foo": {"baz": 1}}, 2, 3, ignore=True)
        2
    """
    _ignore: bool = kwargs.get("ignore", False)
    _search, _else = split(search, ".", maxsplit=1)
    if _search in content and isinstance(content, dict):
        if not _else:
            return content[_search]
        if isinstance((result := content[_search]), dict):
            return getdot(_else, result, *args, **kwargs)
        if _ignore:
            return None
        raise ValueError(f"{_else!r} does not exists in {result}")
    if args:
        return args[0]
    elif _ignore:
        return None
    raise ValueError(f"{_search} does not exists in {content}")


def setdot(search: str, content: dict, value: Any, **kwargs) -> Dict:
    """
    .. usage:
        >>> setdot('data.value', {'data': {'value': 1}}, 2)
        {'data': {'value': 2}}
        >>> setdot('data.value.key', {'data': {'value': 1}}, 2, ignore=True)
        {'data': {'value': 1}}
    """
    _ignore: bool = kwargs.get("ignore", False)
    _search, _else = split(search, ".", maxsplit=1)
    if _search in content and isinstance(content, dict):
        if not _else:
            content[_search] = value
            return content
        if isinstance((result := content[_search]), dict):
            content[_search] = setdot(_else, result, value, **kwargs)
            return content
        if _ignore:
            return content
        raise ValueError(f"{_else!r} does not exists in {result}")
    if _ignore:
        return content
    raise ValueError(f"{_search} does not exists in {content}")


def filter_dict(
    value: Dict[Any, Any],
    included: Optional[Collection] = None,
    excluded: Optional[Collection] = None,
):
    """
    .. usage:
        >>> filter_dict({"foo": "bar"}, included={}, excluded={"foo"})
        {}

        >>> filter_dict(
        ...     {"foo": 1, "bar": 2, "baz": 3},
        ...     included=("foo", )
        ... )
        {'foo': 1}
    """
    _exc = excluded or ()
    return dict(
        filter(
            lambda i: i[0]
            in (v for v in (included or value.keys()) if v not in _exc),
            value.items(),
        )
    )


def size(value: Any) -> int:
    """Recursively iterate to sum size of object & members.

        Empty
        Bytes  type        scaling notes
        28     int         +4 bytes about every 30 powers of 2
        37     bytes       +1 byte per additional byte
        49     str         +1-4 per additional character (depending on max width)
        48     tuple       +8 per additional item
        64     list        +8 for each additional
        224    set         5th increases to 736; 21nd, 2272; 85th, 8416; 341, 32992
        240    dict        6th increases to 368; 22nd, 1184; 43rd, 2280; 86th,
                            4704; 171st, 9320
        136    func def    does not include default args and other attrs
        1056   class def   no slots
        56     class inst  has a __dict__ attr, same scaling as dict above
        888    class def   with slots
        16     __slots__   seems to store in mutable tuple-like structure
                            first slot grows to 48, and so on.

    .. usage:
        >>> size({'foo': 'bar'})
        336
        >>> size('foo')
        52
    """
    _seen_ids = set()

    def inner(obj):
        obj_id = id(obj)
        if obj_id in _seen_ids:
            return 0
        _seen_ids.add(obj_id)
        _size = sys.getsizeof(obj)
        if isinstance(obj, ZERO_DEPTH_BASES):
            # bypass remaining control flow and return
            pass
        elif isinstance(obj, (tuple, list, Set, deque)):
            _size += sum(inner(i) for i in obj)
        elif isinstance(obj, Mapping) or hasattr(obj, "items"):
            _size += sum(inner(k) + inner(v) for k, v in obj.items())
        # Check for custom object instances - may subclass above too
        if hasattr(obj, "__dict__"):
            _size += inner(vars(obj))
        if hasattr(obj, "__slots__"):  # can have __slots__ with __dict__
            _size += sum(
                inner(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s)
            )
        return _size

    return inner(value)
