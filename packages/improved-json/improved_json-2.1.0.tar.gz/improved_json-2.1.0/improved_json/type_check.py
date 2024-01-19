"""
Extend simple_type_check's default type checker to support JsonType and ImprovedJsonType
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from simple_type_check import TypeChecker, TopLevelCheck

from .types import ImprovedJsonType, JsonType

if TYPE_CHECKING:
    from typing import Any


class JsonChecker(TopLevelCheck):
    """
    A type checker for JsonType
    """

    def __call__(self, obj: Any, type_: Any) -> bool:
        return type_ == "JsonType" and self._recurse(obj, JsonType)


class ImprovedJsonChecker(TopLevelCheck):
    """
    A type checker for ImprovedJsonType
    """

    def __call__(self, obj: Any, type_: Any) -> bool:
        return type_ == "ImprovedJsonType" and self._recurse(obj, ImprovedJsonType)


type_check = TypeChecker(advanced=(JsonChecker, ImprovedJsonChecker))
