from __future__ import annotations

from src.parser.ir import ModelIR


def build_model_context(model: ModelIR) -> str:
    """Build a structured description of the model for the LLM."""
    lines = [f"## System: {model.name}", f"{model.description}", ""]

    lines.append("## Entities")
    for entity in model.entities:
        lines.append(f"\n### {entity.name} (table: {entity.table_name})")
        lines.append("Attributes:")
        for attr in entity.attributes:
            meta = []
            if attr.primary_key:
                meta.append("PK")
            if attr.required:
                meta.append("required")
            if attr.unique:
                meta.append("unique")
            if attr.nullable:
                meta.append("nullable")
            meta_str = f" [{', '.join(meta)}]" if meta else ""
            lines.append(f"  - {attr.name}: {attr.type.value}{meta_str}")
        if entity.relationships:
            lines.append("Relationships:")
            for rel in entity.relationships:
                lines.append(f"  - {rel.type.value} -> {rel.target}")
    lines.append("")

    lines.append("## Business Rules")
    for rule in model.business_rules:
        lines.append(f"### {rule.name} ({rule.severity.value})")
        lines.append(f"{rule.description}")
        lines.append("")
    return "\n".join(lines)


FILLER_SYSTEM_PROMPT = """You are a code generation assistant specialized in filling business logic into pre-generated code skeletons.

The code skeleton was generated from a domain model. Files contain `# LLM_FILL:` comments that mark where business logic needs to be inserted.

## Rules
1. ONLY modify code at or directly after `# LLM_FILL:` comment markers. Do NOT change any other code.
2. Implement the business rules described below. Each rule must be enforced at the appropriate LLM_FILL marker.
3. Use the database models and schemas already defined in the skeleton. Do NOT create new models.
4. Return the COMPLETE file with markers filled. Do not truncate or abbreviate.
5. Use proper error handling: raise HTTPException with appropriate status codes (400, 404, 409, 422).
6. Write production-quality code: validate inputs, handle edge cases, use clear variable names.

## Response Format
Return only the complete file content. Start your response with the file's first line.
Do NOT wrap in markdown code blocks. Do NOT add explanations."""


BASELINE_SYSTEM_PROMPT = """You are a full-stack web application generator. You generate complete, working applications from natural language descriptions.

## Tech Stack
- Backend: Python FastAPI with SQLAlchemy + SQLite
- Frontend: React + TypeScript (single-page app, no framework required)
- API communication: fetch() with JSON

## Output Format
Generate EACH file wrapped in markers like this:

###FILE: backend/main.py
```python
(complete file content)
```

###FILE: frontend/App.tsx
```typescript
(complete file content)
```

## Required Files
You MUST generate ALL of the following files:
1. backend/main.py - FastAPI entry point with CORS, DB init
2. backend/models.py - SQLAlchemy models
3. backend/schemas.py - Pydantic request/response schemas
4. backend/routes.py - All CRUD API endpoints with business logic
5. frontend/App.tsx - React app with routing
6. frontend/pages/ - One ListPage and one FormPage per entity
7. frontend/api.ts - API client functions

## Requirements
- Use SQLite (sqlite:///./app.db)
- Include CORS for localhost:3000 and localhost:5173
- Implement complete CRUD for all entities
- Implement all business rules described in the requirements
- React components must handle loading, error, and empty states
- Forms must have client-side validation
- Use React Router for navigation
- Generate complete, working code — no placeholders, no TODOs, no abbreviations"""


FEEDBACK_FIX_PROMPT = """You are fixing errors in generated code. The code below has errors that need to be fixed.

## Model Context
{model_context}

## Error Messages
{errors}

## Failing Code
```
{code}
```

## Instructions
1. Analyze the errors carefully
2. Fix the minimum amount of code to resolve ALL errors
3. If the error is about a missing import, add it
4. If the error is about incorrect logic, fix it
5. Do NOT restructure or refactor the code beyond what's needed
6. Maintain consistency with the model context above

Return the COMPLETE fixed file. Start from the first line. Do NOT wrap in markdown."""
