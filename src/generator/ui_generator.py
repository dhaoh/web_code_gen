from __future__ import annotations

from pathlib import Path

from src.generator.engine import render_template
from src.parser.ir import ModelIR


_FRONTEND_APP_FILES = [
    ("react/api.ts.j2", "api.ts"),
    ("react/App.tsx.j2", "App.tsx"),
    ("react/main.tsx.j2", "main.tsx"),
]

_FRONTEND_CONFIG_FILES = [
    ("react/package.json.j2", "package.json"),
    ("react/tsconfig.json.j2", "tsconfig.json"),
    ("react/vite.config.ts.j2", "vite.config.ts"),
    ("react/index.html.j2", "index.html"),
]


def generate_ui(model: ModelIR, output_dir: str | Path) -> Path:
    output_dir = Path(output_dir)
    pages_dir = output_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    # App source files
    for template_path, filename in _FRONTEND_APP_FILES:
        content = render_template(template_path, model=model)
        (output_dir / filename).write_text(content, encoding="utf-8")

    # Build config files
    for template_path, filename in _FRONTEND_CONFIG_FILES:
        content = render_template(template_path, model=model)
        (output_dir / filename).write_text(content, encoding="utf-8")

    # Entity pages
    for entity in model.entities:
        list_content = render_template("react/ListPage.tsx.j2", entity=entity)
        (pages_dir / f"{entity.name}ListPage.tsx").write_text(list_content, encoding="utf-8")

        form_content = render_template("react/FormPage.tsx.j2", entity=entity)
        (pages_dir / f"{entity.name}FormPage.tsx").write_text(form_content, encoding="utf-8")

    return output_dir
