from base64 import a85encode, a85decode
from pathlib import Path
from typing import cast

from .types import JsonType, ImprovedJsonType


def encode(o: JsonType) -> ImprovedJsonType:
    """
    Convert a JsonType object to an ImprovedJsonType object
    """
    return cast(ImprovedJsonType, _replace(o, True))


def decode(o: ImprovedJsonType) -> JsonType:
    """
    Convert an ImprovedJsonType object to a JsonType object
    """
    return cast(JsonType, _replace(o, False))


#
# Helpers
#


PATH_PREFIX = "Path s#*E3|: "
BYTES_PREFIX_TXT = "BytesT &%d3: "
BYTES_PREFIX_ENC = "BytesE w&>1: "


def _encode_item(o: JsonType) -> ImprovedJsonType:
    if isinstance(o, str):
        if o.startswith(PATH_PREFIX):
            return Path(o[len(PATH_PREFIX) :])
        if o.startswith(BYTES_PREFIX_TXT):
            return o[len(BYTES_PREFIX_TXT) :].encode()
        if o.startswith(BYTES_PREFIX_ENC):
            return a85decode(o[len(BYTES_PREFIX_ENC) :])
    return cast(ImprovedJsonType, o)


def _decode_item(o: ImprovedJsonType) -> JsonType:
    if isinstance(o, Path):
        return f"{PATH_PREFIX}{o}"
    if isinstance(o, bytes):
        try:
            return BYTES_PREFIX_TXT + o.decode()
        except UnicodeDecodeError:
            return BYTES_PREFIX_ENC + a85encode(o).decode()
    return cast(JsonType, o)


def _replace(o: JsonType | ImprovedJsonType, enc: bool) -> JsonType | ImprovedJsonType:
    # Recursive step
    if isinstance(o, dict):
        return {_replace(i, enc): _replace(k, enc) for i, k in o.items()}  # type: ignore
    if isinstance(o, (tuple, list)):  # Support tuples to be nice
        return type(o)(_replace(i, enc) for i in o)  # type: ignore
    # Coding step
    return (_encode_item if enc else _decode_item)(o)  # type: ignore
