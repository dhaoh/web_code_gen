from __future__ import annotations

import re
from pathlib import Path

from src.llm.client import call_llm
from src.llm.prompts import BASELINE_SYSTEM_PROMPT, build_model_context
from src.parser.ir import ModelIR


def generate_from_description(
    model: ModelIR,
    output_dir: str | Path,
    *,
    temperature: float = 0.3,
) -> Path:
    model_context = build_model_context(model)
    nl_description = _build_nl_description(model)

    response = call_llm(
        system_prompt=BASELINE_SYSTEM_PROMPT,
        user_prompt=nl_description,
        temperature=temperature,
        max_tokens=16384,
    )

    files = _parse_files(response)
    _write_files(files, output_dir)
    return Path(output_dir)


def _build_nl_description(model: ModelIR) -> str:
    lines = [
        f"Build a complete web application for: {model.name}",
        "",
        model.description,
        "",
        "## Data Model",
    ]
    for entity in model.entities:
        lines.append(f"\n### {entity.name}")
        lines.append("Attributes:")
        for attr in entity.attributes:
            pk = " (Primary Key, auto-generated)" if attr.primary_key else ""
            req = "Required" if attr.required else "Optional"
            uniq = ", Unique" if attr.unique else ""
            lines.append(f"  - {attr.name}: {attr.type.value} ({req}{uniq}{pk})")
        for rel in entity.relationships:
            lines.append(f"  - Relationship: {rel.type.value} to {rel.target}")

    lines.append("\n## Business Rules (MUST implement)")
    for rule in model.business_rules:
        lines.append(f"\n### {rule.name} ({rule.severity.value})")
        lines.append(f"  {rule.description.strip()}")

    lines.append("\n\nGenerate ALL files. Complete, working code — no placeholders.")
    return "\n".join(lines)


def _parse_files(response: str) -> dict[str, str]:
    """Parse LLM response into filename -> content mapping."""
    files: dict[str, str] = {}
    pattern = r"###FILE:\s*(.+?)\n```(?:\w+)?\n(.*?)```"
    matches = re.findall(pattern, response, re.DOTALL)
    for filename, content in matches:
        files[filename.strip()] = content.strip()
    if not files:
        raise RuntimeError(
            "Failed to parse files from LLM baseline response. "
            f"Response starts with: {response[:200]}..."
        )
    return files


def _write_files(files: dict[str, str], output_dir: str | Path) -> None:
    output_dir = Path(output_dir)
    for filename, content in files.items():
        file_path = output_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
