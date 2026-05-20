import tempfile
from pathlib import Path

import pytest

from src.parser.parser import parse_model
from src.feedback.loop import _check_code


MODELS_DIR = Path(__file__).parent.parent / "models"


class TestCodeChecker:
    def test_valid_code_no_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            # Use a valid module without main.py to test syntax-only path
            (out / "utils.py").write_text("def add(a, b):\n    return a + b\n")
            errors = _check_code(out)
            assert len(errors) == 0

    def test_syntax_error_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            (out / "bad.py").write_text("def broken(:\n    pass\n")
            errors = _check_code(out)
            assert len(errors) > 0

    def test_multiple_files_checked(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            (out / "a.py").write_text("x = 1\n")
            (out / "b.py").write_text("y = 2\n")
            errors = _check_code(out)
            assert len(errors) == 0
