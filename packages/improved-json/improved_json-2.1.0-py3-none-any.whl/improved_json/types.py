from pathlib import Path

JsonType = None | str | int | float | bool | dict[str, "JsonType"] | list["JsonType"]
ImprovedJsonType = (
    None
    | str
    | int
    | float
    | bool
    | dict[str | bytes | Path, "ImprovedJsonType"]
    | list["ImprovedJsonType"]
    | Path
    | bytes
)
