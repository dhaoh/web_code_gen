from __future__ import annotations

import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


_TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"

_engine = Environment(
    loader=FileSystemLoader(str(_TEMPLATES_DIR)),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)

# Type mapping filters
_SQL_TYPE = {
    "integer": "INTEGER",
    "string": "TEXT",
    "float": "REAL",
    "boolean": "INTEGER",
    "datetime": "TEXT",
}

_PY_TYPE = {
    "integer": "int",
    "string": "str",
    "float": "float",
    "boolean": "bool",
    "datetime": "datetime",
}

_TS_TYPE = {
    "integer": "number",
    "string": "string",
    "float": "number",
    "boolean": "boolean",
    "datetime": "string",
}


def sql_type(attr_type: str) -> str:
    return _SQL_TYPE.get(attr_type, "TEXT")


def py_type(attr_type: str) -> str:
    return _PY_TYPE.get(attr_type, "str")


def ts_type(attr_type: str) -> str:
    return _TS_TYPE.get(attr_type, "str")


def to_camel(snake_str: str) -> str:
    parts = snake_str.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])


def to_pascal(snake_str: str) -> str:
    return "".join(p.title() for p in snake_str.split("_"))


def to_title(snake_str: str) -> str:
    return snake_str.replace("_", " ").title()


def plural(name: str) -> str:
    name_lower = name.lower()
    if name_lower.endswith("y") and not name_lower.endswith(("ay", "ey", "oy", "uy")):
        return name[:-1] + "ies"
    if name_lower.endswith(("s", "x", "z", "ch", "sh")):
        return name + "es"
    return name + "s"


_engine.filters["sql_type"] = sql_type
_engine.filters["py_type"] = py_type
_engine.filters["ts_type"] = ts_type
_engine.filters["to_camel"] = to_camel
_engine.filters["to_pascal"] = to_pascal
_engine.filters["to_title"] = to_title
_engine.filters["plural"] = plural


def render_template(template_path: str, **kwargs) -> str:
    template = _engine.get_template(template_path)
    return template.render(**kwargs)
