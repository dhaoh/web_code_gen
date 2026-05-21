from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from src.config import MAX_FEEDBACK_ITERATIONS
from src.llm.client import call_llm
from src.llm.prompts import FEEDBACK_FIX_PROMPT, build_model_context
from src.parser.ir import ModelIR


@dataclass
class FeedbackResult:
    iterations: int = 0
    errors_per_iteration: list[dict] = field(default_factory=list)
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

        file_errors = _check_code(code_dir)
        result.errors_per_iteration.append(file_errors)

        if not file_errors:
            result.final_pass = True
            break

        if iteration < max_iterations:
            _fix_errors(model_context, code_dir, file_errors)

    result.final_output = str(code_dir)
    return result


def _check_code(code_dir: Path) -> dict[str, list[str]]:
    """Check code for errors. Returns {filename: [error_messages]}."""
    file_errors: dict[str, list[str]] = {}

    for py_file in sorted(code_dir.glob("**/*.py")):
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(py_file)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                file_errors.setdefault(str(py_file), []).append(
                    f"Syntax: {result.stderr.strip()[:300]}"
                )
        except subprocess.TimeoutExpired:
            file_errors.setdefault(str(py_file), []).append("Compilation timed out")

    # Check if main.py can be imported successfully
    main_py = code_dir / "main.py"
    if not main_py.exists():
        # Search recursively
        candidates = list(code_dir.rglob("main.py"))
        if candidates:
            main_py = candidates[0]

    main_dir = main_py.parent if main_py.exists() else code_dir
    if main_py.exists():
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    f"import sys; sys.path.insert(0, '{main_dir}'); "
                    "from main import app",
                ],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(main_dir),
            )
            if result.returncode != 0:
                err_msg = result.stderr.strip()
                # Try to determine which file caused the import error
                for py_file in sorted(code_dir.glob("**/*.py")):
                    if py_file.name in err_msg:
                        file_errors.setdefault(str(py_file), []).append(
                            f"Import: {err_msg[:500]}"
                        )
                        break
                else:
                    # Attribute to main.py if can't determine
                    file_errors.setdefault(str(main_py), []).append(
                        f"Import: {err_msg[:500]}"
                    )
        except subprocess.TimeoutExpired:
            file_errors.setdefault(str(main_py), []).append("Import check timed out")

    return file_errors


def _fix_errors(
    model_context: str,
    code_dir: Path,
    file_errors: dict[str, list[str]],
) -> None:
    """Fix ONLY files that have errors. Do not modify error-free files."""
    for file_path_str, errors in file_errors.items():
        py_file = Path(file_path_str)
        if not py_file.exists():
            continue

        original = py_file.read_text(encoding="utf-8")
        error_text = "\n".join(errors)

        user_prompt = FEEDBACK_FIX_PROMPT.format(
            model_context=model_context,
            errors=error_text,
            code=original,
        )

        try:
            fixed = call_llm(
                system_prompt=(
                    "You are a code fixing assistant. Fix ONLY the errors listed below. "
                    "Do NOT add new functionality. Do NOT add package installation code. "
                    "Do NOT add try/except imports. Do NOT modify imports unless they cause "
                    "the specific error. Make the MINIMAL change needed."
                ),
                user_prompt=user_prompt,
                temperature=0.1,
            )
            fixed = fixed.strip()
            if fixed.startswith("```"):
                first_nl = fixed.find("\n")
                if first_nl != -1:
                    fixed = fixed[first_nl + 1:]
                if fixed.endswith("```"):
                    fixed = fixed[: fixed.rfind("```")].strip()
            # Only write if the fix started from the original file's header
            original_header = original.strip().split("\n")[0][:20].strip()
            if fixed.startswith(original_header) or len(fixed) > len(original) * 0.5:
                py_file.write_text(fixed, encoding="utf-8")
        except Exception:
            continue
