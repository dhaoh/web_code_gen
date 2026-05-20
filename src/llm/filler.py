from __future__ import annotations

from pathlib import Path

from src.llm.client import call_llm
from src.llm.prompts import FILLER_SYSTEM_PROMPT, build_model_context
from src.parser.ir import ModelIR


def fill_skeleton(model: ModelIR, skeleton_dir: str | Path) -> Path:
    skeleton_dir = Path(skeleton_dir)
    model_context = build_model_context(model)

    py_files = sorted(skeleton_dir.glob("**/*.py"))
    markers_found = False

    for file_path in py_files:
        content = file_path.read_text(encoding="utf-8")
        if "# LLM_FILL:" not in content:
            continue
        markers_found = True

        filled = call_llm(
            system_prompt=FILLER_SYSTEM_PROMPT,
            user_prompt=_build_filler_user_prompt(model_context, file_path.name, content),
            temperature=0.2,
        )
        filled = _clean_llm_output(filled, content)
        file_path.write_text(filled, encoding="utf-8")

    if not markers_found:
        raise RuntimeError(f"No # LLM_FILL: markers found in {skeleton_dir}")

    return skeleton_dir


def _build_filler_user_prompt(
    model_context: str,
    filename: str,
    content: str,
) -> str:
    return f"""## Model Context
{model_context}

## File to Fill: {filename}
This file has `# LLM_FILL:` markers where business logic needs to be added.

## Instructions
Fill in all `# LLM_FILL:` markers with correct business logic. Implement every business rule
that applies to the entities in this file. Use proper error handling and validation.

Return the COMPLETE file with all markers filled.

```python
{content}
```"""


def _clean_llm_output(output: str, original: str) -> str:
    """Clean LLM output: remove markdown wrappers, ensure it starts correctly."""
    output = output.strip()
    # Remove leading/trailing ``` fences
    if output.startswith("```"):
        first_newline = output.find("\n")
        if first_newline != -1:
            output = output[first_newline + 1 :]
        if output.endswith("```"):
            output = output[: output.rfind("```")].strip()
    # If LLM stripped the start, prepend from original
    if not output.startswith(original.split("\n")[0][:20]):
        output = original.split("\n")[0] + "\n" + output
    return output
