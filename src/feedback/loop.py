from __future__ import annotations

import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from src.config import MAX_FEEDBACK_ITERATIONS
from src.llm.client import call_llm
from src.llm.prompts import FEEDBACK_FIX_PROMPT, build_model_context
from src.parser.ir import ModelIR


@dataclass
class FeedbackResult:
    iterations: int = 0
    errors_per_iteration: list[list[str]] = field(default_factory=list)
    final_pass: bool = False
    final_output: str = ""


def run_feedback_loop(
    model: ModelIR,
    code_dir: str | Path,
    *,
    max_iterations: int = MAX_FEEDBACK_ITERATIONS,
) -> FeedbackResult:
    code_dir = Path(code_dir)
    model_context = build_model_context(model)
    result = FeedbackResult()

    for iteration in range(1, max_iterations + 1):
        result.iterations = iteration

        errors = _check_code(code_dir)
        result.errors_per_iteration.append(errors)

        if not errors:
            result.final_pass = True
            break

        if iteration < max_iterations:
            _fix_errors(model_context, code_dir, errors)

    result.final_output = str(code_dir)
    return result


def _check_code(code_dir: Path) -> list[str]:
    errors: list[str] = []

    # Check Python syntax
    for py_file in sorted(code_dir.glob("**/*.py")):
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(py_file)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                errors.append(f"[{py_file.name}] Syntax: {result.stderr.strip()[:300]}")
        except subprocess.TimeoutExpired:
            errors.append(f"[{py_file.name}] Compilation timed out")

    # Check imports (try importing the main module)
    main_py = code_dir / "main.py"
    if main_py.exists():
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    f"import sys; sys.path.insert(0, '{code_dir}'); "
                    "from main import app",
                ],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(code_dir),
            )
            if result.returncode != 0:
                errors.append(f"[import] {result.stderr.strip()[:500]}")
        except subprocess.TimeoutExpired:
            errors.append("[import] Timed out")

    return errors


def _fix_errors(
    model_context: str,
    code_dir: Path,
    errors: list[str],
) -> None:
    error_text = "\n".join(errors)

    for py_file in sorted(code_dir.glob("**/*.py")):
        original = py_file.read_text(encoding="utf-8")

        user_prompt = FEEDBACK_FIX_PROMPT.format(
            model_context=model_context,
            errors=error_text,
            code=original,
        )

        try:
            fixed = call_llm(
                system_prompt="You are a code fixing assistant. Fix the provided code to resolve all listed errors while maintaining the model constraints.",
                user_prompt=user_prompt,
                temperature=0.1,
            )
            # Clean output
            fixed = fixed.strip()
            if fixed.startswith("```"):
                first_nl = fixed.find("\n")
                if first_nl != -1:
                    fixed = fixed[first_nl + 1 :]
                if fixed.endswith("```"):
                    fixed = fixed[: fixed.rfind("```")].strip()
            if fixed.startswith(original.split("\n")[0][:15]):
                py_file.write_text(fixed, encoding="utf-8")
        except Exception:
            continue
