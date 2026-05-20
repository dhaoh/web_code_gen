import tempfile
from pathlib import Path

import pytest

from src.parser.parser import parse_model
from src.generator.sql_generator import generate_sql
from src.generator.api_generator import generate_api
from src.generator.ui_generator import generate_ui


MODELS_DIR = Path(__file__).parent.parent / "models"


@pytest.fixture
def small_model():
    return parse_model(MODELS_DIR / "small.yaml")


class TestSQLGenerator:
    def test_generates_sql(self, small_model):
        with tempfile.TemporaryDirectory() as tmp:
            out = generate_sql(small_model, tmp)
            assert out.exists()
            content = out.read_text()
            assert "CREATE TABLE IF NOT EXISTS students" in content
            assert "CREATE TABLE IF NOT EXISTS courses" in content
            assert "CREATE TABLE IF NOT EXISTS enrollments" in content
            assert "PRIMARY KEY AUTOINCREMENT" in content

    def test_generates_sql_medium(self):
        model = parse_model(MODELS_DIR / "medium.yaml")
        with tempfile.TemporaryDirectory() as tmp:
            out = generate_sql(model, tmp)
            content = out.read_text()
            assert "CREATE TABLE" in content
            assert "users" in content.lower()
            assert "departments" in content.lower()
            assert "grades" in content.lower()


class TestAPIGenerator:
    def test_generates_api_files(self, small_model):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = generate_api(small_model, tmp)
            files = [f.name for f in out_dir.glob("*.py")]
            assert "main.py" in files
            assert "models.py" in files
            assert "routes.py" in files
            assert "schemas.py" in files

    def test_routes_contain_crud(self, small_model):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = generate_api(small_model, tmp)
            routes = (out_dir / "routes.py").read_text()
            assert "@router_" in routes or "def list_" in routes
            assert "def get_" in routes
            assert "def create_" in routes
            assert "def update_" in routes
            assert "def delete_" in routes

    def test_routes_have_llm_fill_markers(self, small_model):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = generate_api(small_model, tmp)
            routes = (out_dir / "routes.py").read_text()
            assert "# LLM_FILL:" in routes

    def test_schemas_define_pydantic_models(self, small_model):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = generate_api(small_model, tmp)
            schemas = (out_dir / "schemas.py").read_text()
            assert "class StudentBase" in schemas
            assert "class StudentCreate" in schemas
            assert "class StudentResponse" in schemas
            assert "class CourseBase" in schemas


class TestUIGenerator:
    def test_generates_ui_files(self, small_model):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = generate_ui(small_model, tmp)
            files = [f.name for f in out_dir.glob("*.*")]
            assert "App.tsx" in files
            assert "api.ts" in files

    def test_generates_pages_per_entity(self, small_model):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = generate_ui(small_model, tmp)
            pages = [f.name for f in (out_dir / "pages").glob("*")]
            assert "StudentListPage.tsx" in pages
            assert "StudentFormPage.tsx" in pages
            assert "CourseListPage.tsx" in pages
            assert "CourseFormPage.tsx" in pages

    def test_components_import_react(self, small_model):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = generate_ui(small_model, tmp)
            list_page = (out_dir / "pages" / "CourseListPage.tsx").read_text()
            assert "React" in list_page or "react" in list_page.lower()
