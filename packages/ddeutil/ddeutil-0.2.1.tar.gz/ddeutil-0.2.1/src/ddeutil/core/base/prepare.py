from math import ceil


def round_up(number: float, decimals):
    """
    .. usage::
        >>> round_up(1.00406, 2)
        1.01

        >>> round_up(1.00001, 1)
        1.1
    """
    assert isinstance(number, float)
    assert isinstance(decimals, int)
    assert decimals >= 0
    if decimals == 0:
        return ceil(number)
    factor = 10**decimals
    return ceil(number * factor) / factor


def remove_pad(value: str) -> str:
    """Remove zero padding of string
    :usage:
        >>> remove_pad('000')
        '0'

        >>> remove_pad('0123')
        '123'
    """
    return _last_char if (_last_char := value[-1]) == "0" else value.lstrip("0")
