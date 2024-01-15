import importlib
import operator
import sys
import typing
from collections.abc import Callable

from .cache import (
    clear_cache,
    memoize,
    memoized_property,
)
from .checker import (
    can_int,
    # Check type of any value
    is_int,
)
from .convert import (
    # Expectation types
    must_bool,
    must_list,
    str2any,
    str2args,
    str2bool,
    str2dict,
    # Covert string to any types
    str2int_float,
    str2list,
)
from .elements import (
    filter_dict,
    getdot,
    hasdot,
    only_one,
    setdot,
    size,
)
from .hash import (
    checksum,
    freeze,
    freeze_args,
    hash_all,
    hash_pwd,
    hash_str,
    hash_str_by_salt,
    is_same_pwd,
    random_string,
    tokenize,
)
from .merge import (
    merge_dict,
    merge_dict_value,
    merge_dict_values,
    merge_list,
    merge_values,
    zip_equal,
)
from .prepare import (
    remove_pad,
    round_up,
)
from .sorting import (
    ordered,
    reverse_mapping,
    reverse_non_unique_mapping,
    sort_list_by_priority,
)
from .splitter import (
    isplit,
    rsplit,
    split,
    split_str,
)

concat: typing.Callable[[typing.Any], str] = "".join


def operate(x):
    """"""
    return getattr(operator, x)


def is_generic(t: type):
    """Return True if type in the generic alias type."""
    return hasattr(t, "__origin__")


def not_generic(check: typing.Any, instance):
    if instance is typing.NoReturn:
        return check is None
    elif instance is typing.Any:
        return True
    return isinstance(check, instance)


def isinstance_check(check: typing.Any, instance) -> bool:
    """Return True if check data is instance.
    :usage:
        >>> import typing
        >>> assert isinstance_check(['s', ], typing.List[str])
        >>> assert isinstance_check(('s', 't', ), typing.Tuple[str, ...])
        >>> assert not isinstance_check(('s', 't', ), typing.Tuple[str])
        >>> assert isinstance_check({'s': 1, 'd': 'r'}, typing.Dict[str, typing.Union[int, str]])
        >>> assert isinstance_check('s', typing.Optional[str])
        >>> assert isinstance_check(1, typing.Optional[typing.Union[str, int]])
        >>> assert not isinstance_check('s', typing.List[str])
        >>> assert isinstance_check([1, '2'], typing.List[typing.Union[str, int]])
        >>> assert not isinstance_check('s', typing.NoReturn)
        >>> assert isinstance_check(None, typing.NoReturn)
        >>> assert isinstance_check('A', typing.Any)
        >>> assert isinstance_check([1, [1, 2, 3]], typing.List[typing.Union[typing.List[int], int]])
    """
    if not is_generic(instance):
        return not_generic(check, instance)

    origin = typing.get_origin(instance)
    if origin == typing.Union:
        return any(
            isinstance_check(check, typ) for typ in typing.get_args(instance)
        )

    if not issubclass(check.__class__, origin):
        return False

    if origin == dict:
        _dict = typing.get_args(instance)
        return all(
            (isinstance_check(k, _dict[0]) and isinstance_check(v, _dict[1]))
            for k, v in check.items()
        )
    elif origin in {
        tuple,
        list,
    }:
        _dict = typing.get_args(instance)
        if Ellipsis in _dict or (origin is not tuple):
            return all(isinstance_check(i, _dict[0]) for i in iter(check))
        try:
            return all(
                isinstance_check(i[0], i[1]) for i in zip_equal(check, _dict)
            )
        except ValueError:
            return False
    elif origin is Callable:
        return callable(check)
    raise NotImplementedError("It can not check typing instance of this pair.")


def cached_import(module_path, class_name):
    """Cached import package"""
    modules = sys.modules
    if (
        module_path not in modules
        or getattr(modules[module_path], "__spec__", None) is not None
        and getattr(modules[module_path].__spec__, "_initializing", False)
    ):
        importlib.import_module(module_path)
    return getattr(modules[module_path], class_name)


def import_string(dotted_path):
    """Import a dotted module path and return the attribute/class designated by
    the last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError(
            f"{dotted_path} doesn't look like a module path"
        ) from err

    try:
        return cached_import(module_path, class_name)
    except AttributeError as err:
        raise ImportError(
            f'Module "{module_path}" does not define a "{class_name}" attribute/class'
        ) from err
