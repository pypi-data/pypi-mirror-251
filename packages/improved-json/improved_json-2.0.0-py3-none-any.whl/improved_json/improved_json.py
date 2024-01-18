from pathlib import Path
from typing import Any
import json

from simple_type_check import type_check

from .types import improved_json_type
from .code import encode, decode


__all__ = (
    "loadf",
    "dumpf",
    "loads",
    "dumps",
)


def loadf(path: str | Path, *args, **kwargs) -> improved_json_type:
    """
    A wrapper around loads that loads the data field from the given file path
    Other arguments are otherwise passed through to loads
    :param path: The file path to load
    """
    if isinstance(path, str):
        path = Path(path)
    with path.open("r") as f:
        data = f.read()
    return loads(data, *args, **kwargs)


def dumpf(path: str | Path, *args, **kwargs) -> int:
    """
    A wrapper around dumps that outputs the data to the given path
    Other arguments are otherwise passed through to dumps
    :param path: The file path to write to
    :return: The number of bytes written
    """
    out: str = dumps(*args, **kwargs)
    if isinstance(path, str):
        path = Path(path)
    with path.open("w") as f:
        return f.write(out)


def loads(data: str | bytes, type_: type | Any = Any, **kwargs) -> improved_json_type:
    """
    Load a json object from the string data
    Other arguments are otherwise passed through to json.loads
    Supports type_ containing some parameterized generic types from the typing module
    Also supports some parameterized generic without parameters (i.e. as generics)
    Raises ValueError if type_ is invalid
    :param data: The string to load
    :param type_: The required return type
    :return: The json object constructed from data
    """
    ret = encode(json.loads(data, **kwargs))
    if not type_check(ret, type_):
        raise TypeError("Return value is not of type: {type_}", ret)
    return ret


def dumps(obj: improved_json_type, **kwargs) -> str:
    """
    Dump the improved json object to a string
    Other arguments are otherwise passed through to json.dumps
    :param obj: The json object to convert to a string
    :return: obj represented as a string
    """
    return json.dumps(decode(obj), **kwargs)
