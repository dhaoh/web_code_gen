from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AttributeType(str, Enum):
    INTEGER = "integer"
    STRING = "string"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATETIME = "datetime"


class RelationshipType(str, Enum):
    MANY_TO_ONE = "many_to_one"
    ONE_TO_MANY = "one_to_many"
    MANY_TO_MANY = "many_to_many"


class Severity(str, Enum):
    CRITICAL = "critical"
    IMPORTANT = "important"
    NICE_TO_HAVE = "nice_to_have"


class Attribute(BaseModel):
    name: str
    type: AttributeType
    primary_key: bool = False
    required: bool = False
    unique: bool = False
    nullable: bool = False
    default: Any = None
    max_length: int | None = None


class Relationship(BaseModel):
    type: RelationshipType
    target: str
    foreign_key: str | None = None
    back_populates: str | None = None
    through: str | None = None


class Entity(BaseModel):
    name: str
    attributes: list[Attribute] = Field(default_factory=list)
    relationships: list[Relationship] = Field(default_factory=list)

    @property
    def primary_key_attr(self) -> Attribute | None:
        for a in self.attributes:
            if a.primary_key:
                return a
        return None

    @property
    def required_attrs(self) -> list[Attribute]:
        return [a for a in self.attributes if a.required]

    @property
    def table_name(self) -> str:
        return self.name.lower() + "s"


class BusinessRule(BaseModel):
    name: str
    description: str
    severity: Severity = Severity.IMPORTANT


class ModelIR(BaseModel):
    name: str
    description: str = ""
    entities: list[Entity] = Field(default_factory=list)
    business_rules: list[BusinessRule] = Field(default_factory=list)

    def get_entity(self, name: str) -> Entity | None:
        for e in self.entities:
            if e.name.lower() == name.lower():
                return e
        return None

    def validate_references(self) -> list[str]:
        errors: list[str] = []
        entity_names = {e.name.lower() for e in self.entities}
        for entity in self.entities:
            for rel in entity.relationships:
                if rel.target.lower() not in entity_names:
                    errors.append(
                        f"Entity '{entity.name}' references unknown target "
                        f"'{rel.target}' in relationship"
                    )
                if rel.through and rel.through.lower() not in entity_names:
                    errors.append(
                        f"Entity '{entity.name}' references unknown through "
                        f"table '{rel.through}' in relationship"
                    )
        return errors
