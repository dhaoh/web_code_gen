from pathlib import Path

from src.parser.parser import parse_model


MODELS_DIR = Path(__file__).parent.parent / "models"


def test_parse_small_model():
    model = parse_model(MODELS_DIR / "small.yaml")
    assert model.name == "student_course_system_small"
    assert len(model.entities) == 3
    assert len(model.business_rules) == 2

    student = model.get_entity("Student")
    assert student is not None
    assert len(student.attributes) == 3
    assert student.primary_key_attr.name == "id"
    assert any(a.unique for a in student.attributes)

    errors = model.validate_references()
    assert len(errors) == 0


def test_parse_medium_model():
    model = parse_model(MODELS_DIR / "medium.yaml")
    assert len(model.entities) == 6
    assert len(model.business_rules) == 6
    assert model.validate_references() == []

    # Check relationships
    course = model.get_entity("Course")
    assert course is not None
    rel_targets = [r.target for r in course.relationships]
    assert "Department" in rel_targets
    assert "User" in rel_targets


def test_parse_large_model():
    model = parse_model(MODELS_DIR / "large.yaml")
    assert len(model.entities) == 11
    assert len(model.business_rules) == 10
    assert model.validate_references() == []


def test_entity_properties():
    model = parse_model(MODELS_DIR / "small.yaml")
    student = model.get_entity("Student")
    assert student.table_name == "students"
    required = [a.name for a in student.required_attrs]
    assert "name" in required
    assert "email" in required
