from __future__ import annotations

import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CompilabilityScore:
    python_syntax_pass: bool = False
    python_import_pass: bool = False
    frontend_build_pass: bool = False
    has_frontend: bool = False
    errors: list[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []

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

    # Check Python syntax for all .py files
    py_files = list(code_dir.glob("**/*.py"))
    if py_files:
        all_syntax_ok = True
        for f in py_files:
            try:
                result = subprocess.run(
                    ["python", "-m", "py_compile", str(f)],
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

    # Check if main.py can be imported
    main_py = code_dir / "main.py"
    if main_py.exists():
        try:
            result = subprocess.run(
                [
                    "python",
                    "-c",
                    f"import sys; sys.path.insert(0, '{code_dir}'); "
                    "from main import app; print('OK')",
                ],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(code_dir),
            )
            score.python_import_pass = result.returncode == 0
            if not score.python_import_pass:
                score.errors.append(f"Import: {result.stderr.strip()[:300]}")
        except Exception as e:
            score.errors.append(f"Import exception: {e}")

    # Check frontend
    has_package_json = (code_dir / "package.json").exists()
    has_tsx = bool(list(code_dir.glob("**/*.tsx"))) or bool(list(code_dir.glob("**/*.jsx")))
    score.has_frontend = has_package_json or has_tsx

    if has_package_json:
        try:
            result = subprocess.run(
                ["npm", "install"],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(code_dir),
            )
            if result.returncode == 0:
                result = subprocess.run(
                    ["npm", "run", "build"],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=str(code_dir),
                )
                score.frontend_build_pass = result.returncode == 0
                if not score.frontend_build_pass:
                    score.errors.append(f"Build: {result.stderr.strip()[:300]}")
            else:
                score.errors.append(f"npm install: {result.stderr.strip()[:200]}")
        except Exception as e:
            score.errors.append(f"Frontend exception: {e}")

    return score
