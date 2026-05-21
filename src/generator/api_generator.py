from __future__ import annotations

from pathlib import Path

from src.generator.engine import py_default, py_type
from src.parser.ir import Attribute, Entity, ModelIR


_BACKEND_TEMPLATES = [
    ("fastapi/models.py.j2", "models.py"),
    ("fastapi/routes.py.j2", "routes.py"),
    ("fastapi/main.py.j2", "main.py"),
]


def generate_api(model: ModelIR, output_dir: str | Path) -> Path:
    from src.generator.engine import render_template

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for template_path, filename in _BACKEND_TEMPLATES:
        content = render_template(template_path, model=model)
        out_path = output_dir / filename
        out_path.write_text(content, encoding="utf-8")

    # Generate schemas.py in plain Python for clean formatting
    schemas_content = _generate_schemas(model)
    (output_dir / "schemas.py").write_text(schemas_content, encoding="utf-8")

    # Generate backend requirements.txt
    from src.generator.engine import render_template
    req_content = render_template("fastapi/requirements.txt.j2", model=model)
    (output_dir / "requirements.txt").write_text(req_content, encoding="utf-8")

    return output_dir


def _generate_schemas(model: ModelIR) -> str:
    lines = []
    lines.append('"""')
    lines.append(f"Pydantic schemas for {model.name}.")
    lines.append('Generated from model definition.')
    lines.append('"""')
    lines.append("from datetime import datetime")
    lines.append("from typing import Optional")
    lines.append("from pydantic import BaseModel")
    lines.append("")

    for i, entity in enumerate(model.entities):
        if i > 0:
            lines.append("")
            lines.append("")
        lines.append(f"# --- {entity.name} ---")
        lines.append("")
        # Base
        lines.append(f"class {entity.name}Base(BaseModel):")
        for attr in entity.attributes:
            if not attr.primary_key:
                lines.append(_format_field(attr))
        if not any(not a.primary_key for a in entity.attributes):
            lines.append("    pass")
        lines.append("")
        # Create
        lines.append(f"class {entity.name}Create({entity.name}Base):")
        required_attrs = [a for a in entity.attributes if a.required and not a.primary_key]
        for attr in required_attrs:
            lines.append(_format_field(attr, force_required=True))
        if not required_attrs:
            lines.append("    pass")
        lines.append("")
        # Update
        lines.append(f"class {entity.name}Update(BaseModel):")
        update_attrs = [a for a in entity.attributes if not a.primary_key]
        for attr in update_attrs:
            lines.append(_format_field(attr, optional_with_default=True))
        if not update_attrs:
            lines.append("    pass")
        lines.append("")
        # Response
        lines.append(f"class {entity.name}Response({entity.name}Base):")
        for attr in entity.attributes:
            if attr.primary_key:
                lines.append(f"    {attr.name}: {py_type(attr.type.value)}")
        lines.append("")
        lines.append("    class Config:")
        lines.append("        from_attributes = True")

    return "\n".join(lines)


def _format_field(
    attr: Attribute,
    *,
    force_required: bool = False,
    optional_with_default: bool = False,
) -> str:
    ptype = py_type(attr.type.value)
    suffix = ""

    if optional_with_default:
        if attr.default is not None and attr.default != "CURRENT_TIMESTAMP":
            suffix = f" | None = {py_default(attr.type.value, attr.default)}"
        else:
            suffix = " | None = None"
    elif attr.nullable or (not attr.required and not force_required):
        suffix = " | None = None"
    elif attr.default is not None and attr.default != "CURRENT_TIMESTAMP":
        suffix = f" = {py_default(attr.type.value, attr.default)}"

    return f"    {attr.name}: {ptype}{suffix}"
