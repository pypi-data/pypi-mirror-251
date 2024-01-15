import hashlib
import hmac
import os
import random
import string
import uuid
from base64 import b64encode
from functools import wraps
from typing import (
    Any,
    Collection,
    Optional,
    Tuple,
)

import ujson


def checksum(value: Any) -> str:
    """
    .. usage::
        >>> checksum({"foo": "bar", "baz": 1})
        '83788ce748a5899920673e5a4384979b'
    """
    return hashlib.md5(
        ujson.dumps(value, sort_keys=True).encode("utf-8")
    ).hexdigest()


def hash_all(
    value: Any,
    exclude: Optional[Collection] = None,
):
    """Hash values in dictionary

    .. usage::
        >>> hash_all({'foo': 'bar'})
        {'foo': '37b51d194a7513e45b56f6524f2d51f2'}
    """
    _exclude_keys: Collection = exclude or set()
    if isinstance(value, dict):
        return {
            k: hash_all(v) if k not in _exclude_keys else v
            for k, v in value.items()
        }
    elif isinstance(value, (list, tuple)):
        return type(value)([hash_all(i) for i in value])
    elif isinstance(value, bool):
        return value
    elif isinstance(value, (int, float)):
        value = str(value)
    elif value is None:
        return value
    return hashlib.md5(value.encode("utf-8")).hexdigest()


def hash_str(value: str, length: int = 8) -> str:
    """Hash str input to number with SHA256 algorithm
    more algoritm be md5, sha1, sha224, sha256, sha384, sha512
    :usage:
        >>> hash_str('Hello World')
        '40300654'

        >>> hash_str('hello world')
        '05751529'
    """
    _algorithm: str = "sha256"
    return str(
        int(
            getattr(hashlib, _algorithm)(value.encode("utf-8")).hexdigest(),
            16,
        )
    )[-length:]


def hash_str_by_salt(value):
    """Hash str

    .. usage::
        >>> hash_str_by_salt('P@ssw0rd')
        ('19787c1219844c599915852bdd3ac6df', '7082...f895bb')
    """
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512((value + salt).encode("utf-8")).hexdigest()
    return salt, hashed_password


def hash_pwd(password: str) -> Tuple[bytes, bytes]:
    """Hash the provided password with a randomly-generated salt and return the
    salt and hash to store in the database.

    .. warning::
        - The use of a 16-byte salt and 100000 iterations of PBKDF2 match
          the minimum numbers recommended in the Python docs. Further increasing
          the number of iterations will make your hashes slower to compute,
          and therefore more secure.

    .. ref::
        - https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python/56915300#56915300
    """
    salt = b64encode(os.urandom(16))
    pw_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000,
    )
    return salt, pw_hash


def is_same_pwd(salt: bytes, pw_hash: bytes, password: str) -> bool:
    """Given a previously-stored salt and hash, and a password provided by a user
    trying to log in, check whether the password is correct.

    .. usage::
        >>> s, pw = hash_pwd('P@ssW0rd')
        >>> is_same_pwd(s, pw, 'P@ssW0rd')
        True

    :ref:
        - https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python/56915300#56915300
    """
    return hmac.compare_digest(
        pw_hash, hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    )


def tokenize(*args, **kwargs):
    """Deterministic token (modified from dask.base)
    :usage:
        >>> tokenize([1, 2, '3'])
        '9d71491b50023b06fc76928e6eddb952'

        >>> tokenize('Hello') == tokenize('Hello')
        True
    """
    if kwargs:
        args += (kwargs,)
    try:
        return hashlib.md5(str(args).encode()).hexdigest()
    except ValueError:
        # FIPS systems: https://github.com/fsspec/filesystem_spec/issues/380
        return hashlib.md5(
            str(args).encode(), usedforsecurity=False
        ).hexdigest()


def freeze(value: Any):
    """Freeze the value to immutable
    .. usage::
        >>> freeze({'foo': 'bar'})
        frozenset({('foo', 'bar')})
    """
    if isinstance(value, dict):
        return frozenset((key, freeze(value)) for key, value in value.items())
    elif isinstance(value, list):
        return tuple(freeze(value) for value in value)
    elif isinstance(value, set):
        return frozenset(freeze(value) for value in value)
    return value


def freeze_args(func):
    """Transform mutable dictionary into immutable useful to
    be compatible with cache.

    .. usage::
        >>> from functools import lru_cache
        >>>
        >>> @lru_cache(maxsize=None)
        ... def call_name(value: dict):
        ...     return value['foo'] + " " + value['bar']
        >>> call_name({'foo': 'Hello', 'bar': 'World'})
        Traceback (most recent call last):
        ...
        TypeError: unhashable type: 'dict'

        >>> @freeze_args
        ... @lru_cache(maxsize=None)
        ... def call_name(value: dict):
        ...     return value['foo'] + " " + value['bar']
        >>> call_name({'foo': 'Hello', 'bar': 'World'})
        'Hello World'
    """

    class HashDict(dict):
        def __hash__(self):
            return hash(freeze(self))

    @wraps(func)
    def wrapped(*args, **kwargs):
        args: tuple = tuple(
            HashDict(arg) if isinstance(arg, dict) else arg for arg in args
        )
        kwargs: dict = {
            k: HashDict(v) if isinstance(v, dict) else v
            for k, v in kwargs.items()
        }
        return func(*args, **kwargs)

    return wrapped


def random_string(num_length: int = 8) -> str:
    """Random string from uppercase ASCII and number 0-9"""
    return "".join(
        random.choices(string.ascii_uppercase + string.digits, k=num_length)
    )
