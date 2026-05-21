from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from src.evaluator import iter_code_files


@dataclass
class CompilabilityScore:
    python_syntax_pass: bool = False
    python_import_pass: bool = False
    frontend_build_pass: bool = False
    has_frontend: bool = False
    errors: list[str] = field(default_factory=list)

    @property
    def score(self) -> float:
        if self.has_frontend:
            checks = [self.python_syntax_pass, self.python_import_pass, self.frontend_build_pass]
        else:
            checks = [self.python_syntax_pass, self.python_import_pass]
        return sum(1 for c in checks if c) / len(checks) if checks else 0.0


def evaluate_compilability(code_dir: str | Path) -> CompilabilityScore:
    code_dir = Path(code_dir)
    score = CompilabilityScore()

    # Find backend directory (model_driven uses "backend" subdir, pure_llm puts files in root)
    backend_dir = code_dir / "backend" if (code_dir / "backend").is_dir() else code_dir

    # Check Python syntax for all .py files
    py_files = list(iter_code_files(code_dir, "*.py"))
    if py_files:
        all_syntax_ok = True
        for f in py_files:
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "py_compile", str(f)],
                    capture_output=True,
                    text=True,
                    timeout=15,
                )
                if result.returncode != 0:
                    all_syntax_ok = False
                    score.errors.append(f"{f.name}: {result.stderr.strip()[:200]}")
            except subprocess.TimeoutExpired:
                all_syntax_ok = False
                score.errors.append(f"{f.name}: timeout")
        score.python_syntax_pass = all_syntax_ok
    else:
        score.python_syntax_pass = False
        score.errors.append("No Python files found")

    # Check if main.py exists and can be imported
    main_py = _find_file(code_dir, "main.py")
    if main_py:
        main_dir = main_py.parent
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    f"import sys; sys.path.insert(0, '{main_dir}'); "
                    "from main import app; print('OK')",
                ],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(main_dir),
            )
            score.python_import_pass = result.returncode == 0
            if not score.python_import_pass:
                score.errors.append(f"Import: {result.stderr.strip()[:300]}")
        except Exception as e:
            score.errors.append(f"Import exception: {e}")
    else:
        score.errors.append("No main.py found")

    # Check frontend
    package_json = _find_file(code_dir, "package.json")
    has_tsx = bool(list(iter_code_files(code_dir, "*.tsx"))) or bool(list(iter_code_files(code_dir, "*.jsx")))
    score.has_frontend = package_json is not None or has_tsx

    if package_json:
        try:
            result = subprocess.run(
                ["npm", "install"],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(package_json.parent),
            )
            if result.returncode == 0:
                result = subprocess.run(
                    ["npm", "run", "build"],
                    capture_output=True,
                    text=True,
                    timeout=120,
                    cwd=str(package_json.parent),
                )
                score.frontend_build_pass = result.returncode == 0
                if not score.frontend_build_pass:
                    score.errors.append(f"Build: {result.stderr.strip()[:300]}")
            else:
                score.errors.append(f"npm install: {result.stderr.strip()[:200]}")
        except Exception as e:
            score.errors.append(f"Frontend exception: {e}")

    return score


def _find_file(code_dir: Path, filename: str) -> Path | None:
    """Search for a file recursively, return first match."""
    matches = list(iter_code_files(code_dir, filename))
    return matches[0] if matches else None
