from pathlib import Path

json_type = None | str | int | float | bool | dict[str, "json_type"] | list["json_type"]
improved_json_type = (
    None
    | str
    | int
    | float
    | bool
    | dict[str | bytes | Path, "improved_json_type"]
    | list["improved_json_type"]
    | Path
    | bytes
)
