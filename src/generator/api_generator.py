from __future__ import annotations

from pathlib import Path

from src.generator.engine import render_template
from src.parser.ir import ModelIR


_BACKEND_FILES = [
    ("fastapi/models.py.j2", "models.py"),
    ("fastapi/schemas.py.j2", "schemas.py"),
    ("fastapi/routes.py.j2", "routes.py"),
    ("fastapi/main.py.j2", "main.py"),
]


def generate_api(model: ModelIR, output_dir: str | Path) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rendered_files = {}

    for template_path, filename in _BACKEND_FILES:
        content = render_template(template_path, model=model)
        out_path = output_dir / filename
        out_path.write_text(content, encoding="utf-8")
        rendered_files[filename] = str(out_path)

    return output_dir
