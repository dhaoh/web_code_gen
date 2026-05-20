import tempfile
from pathlib import Path

import pytest

from src.parser.parser import parse_model
from src.evaluator.structure import evaluate_structure, StructureScore
from src.evaluator.compilability import evaluate_compilability, CompilabilityScore
from src.evaluator.consistency import evaluate_consistency


MODELS_DIR = Path(__file__).parent.parent / "models"


@pytest.fixture
def small_model():
    return parse_model(MODELS_DIR / "small.yaml")


class TestStructureEvaluator:
    def test_empty_dir_scores_zero(self, small_model):
        with tempfile.TemporaryDirectory() as tmp:
            score = evaluate_structure(small_model, tmp)
            assert score.score < 1.0

    def test_known_good_code_scores_high(self, small_model):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            (out / "main.py").write_text("""
from fastapi import FastAPI
app = FastAPI()

class Student: pass
class Course: pass
class Enrollment: pass

@router.get("/students")
def list_students(): pass
@router.post("/students")
def create_student(): pass
@router.get("/students/{id}")
def get_student(): pass
@router.put("/students/{id}")
def update_student(): pass
@router.delete("/students/{id}")
def delete_student(): pass
""")
            score = evaluate_structure(small_model, out)
            assert score.entity_count_match
            assert score.table_count_match
            # Should detect at least some endpoints


class TestCompilabilityEvaluator:
    def test_valid_python_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            (out / "main.py").write_text("print('hello')\n")
            score = evaluate_compilability(out)
            assert score.python_syntax_pass

    def test_invalid_python_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            (out / "main.py").write_text("this is not valid python @@@\n")
            score = evaluate_compilability(out)
            assert not score.python_syntax_pass


class TestConsistencyEvaluator:
    def test_identical_dirs_max_similarity(self):
        with tempfile.TemporaryDirectory() as tmp1, tempfile.TemporaryDirectory() as tmp2:
            (Path(tmp1) / "routes.py").write_text("def foo():\n    return 1\n")
            (Path(tmp2) / "routes.py").write_text("def foo():\n    return 1\n")

            score = evaluate_consistency([tmp1, tmp2])
            assert score.average_similarity > 0.95

    def test_different_dirs_low_similarity(self):
        with tempfile.TemporaryDirectory() as tmp1, tempfile.TemporaryDirectory() as tmp2:
            (Path(tmp1) / "routes.py").write_text("def foo():\n    return 1\n")
            (Path(tmp2) / "routes.py").write_text("def bar():\n    x = 2\n    y = 3\n    return x + y\n")

            score = evaluate_consistency([tmp1, tmp2])
            assert score.average_similarity < 0.8
