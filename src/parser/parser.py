from pathlib import Path

import yaml

from src.parser.ir import (
    Attribute,
    AttributeType,
    BusinessRule,
    Entity,
    ModelIR,
    Relationship,
    RelationshipType,
    Severity,
)


def parse_model(file_path: str | Path) -> ModelIR:
    file_path = Path(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    entities = [_parse_entity(e) for e in raw.get("entities", [])]
    rules = [_parse_business_rule(r) for r in raw.get("business_rules", [])]

    model = ModelIR(
        name=raw.get("name", file_path.stem),
        description=raw.get("description", ""),
        entities=entities,
        business_rules=rules,
    )

    ref_errors = model.validate_references()
    if ref_errors:
        raise ValueError("Model reference errors:\n" + "\n".join(ref_errors))

    return model


def _parse_entity(raw: dict) -> Entity:
    attrs = [_parse_attribute(a) for a in raw.get("attributes", [])]
    rels = [_parse_relationship(r) for r in raw.get("relationships", [])]
    return Entity(
        name=raw["name"],
        attributes=attrs,
        relationships=rels,
    )


def _parse_attribute(raw: dict) -> Attribute:
    return Attribute(
        name=raw["name"],
        type=AttributeType(raw["type"]),
        primary_key=raw.get("primary_key", False),
        required=raw.get("required", False),
        unique=raw.get("unique", False),
        nullable=raw.get("nullable", False),
        default=raw.get("default"),
        max_length=raw.get("max_length"),
    )


def _parse_relationship(raw: dict) -> Relationship:
    return Relationship(
        type=RelationshipType(raw["type"]),
        target=raw["target"],
        foreign_key=raw.get("foreign_key"),
        back_populates=raw.get("back_populates"),
        through=raw.get("through"),
    )


def _parse_business_rule(raw: dict) -> BusinessRule:
    return BusinessRule(
        name=raw["name"],
        description=raw.get("description", ""),
        severity=Severity(raw.get("severity", "important")),
    )
