from base64 import a85encode, a85decode
from pathlib import Path
from typing import cast

from .types import json_type, improved_json_type


def encode(o: json_type) -> improved_json_type:
    """
    Convert a json_type object to an improved_json_type object
    """
    return cast(improved_json_type, _replace(o, True))


def decode(o: improved_json_type) -> json_type:
    """
    Convert an improved_json_type object to a json_type object
    """
    return cast(json_type, _replace(o, False))


#
# Helpers
#


PATH_PREFIX = "Path s#*E3|: "
BYTES_PREFIX_TXT = "BytesT &%d3: "
BYTES_PREFIX_ENC = "BytesE w&>1: "


def _encode_item(o: json_type) -> improved_json_type:
    if isinstance(o, str):
        if o.startswith(PATH_PREFIX):
            return Path(o[len(PATH_PREFIX) :])
        if o.startswith(BYTES_PREFIX_TXT):
            return o[len(BYTES_PREFIX_TXT) :].encode()
        if o.startswith(BYTES_PREFIX_ENC):
            return a85decode(o[len(BYTES_PREFIX_ENC) :])
    return cast(improved_json_type, o)


def _decode_item(o: improved_json_type) -> json_type:
    if isinstance(o, Path):
        return f"{PATH_PREFIX}{o}"
    if isinstance(o, bytes):
        try:
            return BYTES_PREFIX_TXT + o.decode()
        except UnicodeDecodeError:
            return BYTES_PREFIX_ENC + a85encode(o).decode()
    return cast(json_type, o)


def _replace(o: json_type | improved_json_type, encode: bool) -> json_type | improved_json_type:
    # Recursive step
    if isinstance(o, dict):
        return {_replace(i, encode): _replace(k, encode) for i, k in o.items()}  # type: ignore
    if isinstance(o, (tuple, list)):  # Support tuples to be nice
        return type(o)(_replace(i, encode) for i in o)  # type: ignore
    # Coding step
    return (_encode_item if encode else _decode_item)(o)  # type: ignore
