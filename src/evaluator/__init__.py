from pathlib import Path

_EXCLUDE_PARTS = {"node_modules", "__pycache__", ".git", "dist", "venv", ".venv", "env", "build"}


def iter_code_files(directory: Path, pattern: str = "*.py"):
    """Iterate source code files, skipping build/install directories."""
    for f in directory.rglob(pattern):
        if any(excl in f.parts for excl in _EXCLUDE_PARTS):
            continue
        yield f
