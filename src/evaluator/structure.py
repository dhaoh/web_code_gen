from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.evaluator import iter_code_files
from src.parser.ir import ModelIR


@dataclass
class StructureScore:
    entity_count_match: bool = False
    endpoint_count_match: bool = False
    table_count_match: bool = False
    frontend_component_count: int = 0
    expected_components: int = 0
    details: dict = None

    @property
    def score(self) -> float:
        checks = [self.entity_count_match, self.endpoint_count_match, self.table_count_match]
        passed = sum(1 for c in checks if c)
        component_score = (
            min(self.frontend_component_count / max(self.expected_components, 1), 1.0)
            * 0.3
        )
        return (passed / len(checks)) * 0.7 + component_score


def evaluate_structure(model: ModelIR, code_dir: str | Path) -> StructureScore:
    code_dir = Path(code_dir)
    score = StructureScore()

    # Count expected
    expected_entities = len(model.entities)
    expected_tables = expected_entities  # One table per entity
    expected_endpoints = expected_entities * 5  # CRUD: list, get, create, update, delete
    expected_components = expected_entities * 2  # List + Form per entity

    # Check generated files
    python_files = list(iter_code_files(code_dir, "*.py"))
    combined_content = ""
    for f in python_files:
        combined_content += f.read_text(encoding="utf-8", errors="ignore") + "\n"

    # Count entity names referenced in code
    entities_found = 0
    for entity in model.entities:
        if entity.name in combined_content:
            entities_found += 1

    # Count SQL tables
    tables_found = 0
    for entity in model.entities:
        if f"class {entity.name}" in combined_content:
            tables_found += 1

    # Count API routes (decorator pattern @router.get, @router.post, etc.)
    import re
    route_pattern = re.compile(r'@router[_\d]*\.\s*(get|post|put|delete|patch)\s*\(', re.IGNORECASE)
    routes_found = len(route_pattern.findall(combined_content))

    # Count frontend components
    tsx_files = list(iter_code_files(code_dir, "*.tsx")) + list(iter_code_files(code_dir, "*.jsx"))
    component_count = len(tsx_files)

    score.entity_count_match = entities_found >= expected_entities
    score.table_count_match = tables_found >= expected_tables
    score.endpoint_count_match = routes_found >= expected_endpoints * 0.8
    score.frontend_component_count = component_count
    score.expected_components = expected_components
    score.details = {
        "entities_expected": expected_entities,
        "entities_found": entities_found,
        "tables_expected": expected_tables,
        "tables_found": tables_found,
        "endpoints_expected": expected_endpoints,
        "endpoints_found": routes_found,
        "frontend_components": component_count,
        "expected_frontend_components": expected_components,
    }

    return score
