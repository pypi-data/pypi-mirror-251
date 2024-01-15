from __future__ import annotations

from typing import (
    Any,
    Tuple,
)

StringTrueLower: Tuple[str, ...] = (
    "yes",
    "y",
    "true",
    "t",
    "1",
    "1.0",
    "o",
)
StringFalseLower: Tuple[str, ...] = (
    "no",
    "n",
    "false",
    "f",
    "0",
    "0.0",
    "x",
)


def is_int(value: Any) -> bool:
    """Check value that is integer

    .. docs::
        https://stackoverflow.com/questions/1265665/
        how-can-i-check-if-a-string-represents-an-int-without-using-try-except

    .. usage::
        >>> is_int('')
        False
        >>> is_int('0.0')
        False
        >>> is_int('-3')
        True
        >>> is_int('-123.4')
        False
        >>> is_int('543')
        True
        >>> is_int('0')
        True
        >>> is_int('-')
        False
    """
    if isinstance(value, int):
        return True

    _value = str(value)
    if not value:
        return False

    # For string type, it has checking methods like:
    # ``str.isdigit()`` or ``str.isdecimal()`` or ``str.isnumeric()``
    return (
        _value[1:].isdecimal()
        if _value[0] in {"-", "+"}
        else _value.isdecimal()
    )


def can_int(value: Any) -> bool:
    """Check value that able to integer
    .. usage:
        >>> can_int('0.0')
        True
        >>> can_int('-1.0')
        True
    """
    try:
        return float(str(value)).is_integer()
    except (TypeError, ValueError):
        return False
