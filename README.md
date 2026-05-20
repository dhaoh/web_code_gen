# Web Application Code Generation: Model-Driven vs Pure LLM

A comparative study of two approaches to AI-assisted code generation for web applications:
- **Model-Driven Method**: Domain models (YAML) define the architecture, LLM fills in business logic within pre-generated code skeletons
- **Pure LLM Method**: Natural language descriptions fed directly to LLM for full-stack code generation


## Architecture

```
YAML Domain Model
       │
       ▼
┌──────────────┐     ┌──────────────────┐
│ Model Parser  │────▶│ Intermediate IR   │
│ (YAML→Pydantic)│    │ (Pydantic models) │
└──────────────┘     └──────┬───────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │SQL Gen   │ │API Gen   │ │UI Gen    │
        │(Jinja2)  │ │(Jinja2)  │ │(Jinja2)  │
        └────┬─────┘ └────┬─────┘ └────┬─────┘
             │            │            │
             └────────────┼────────────┘
                          ▼
                  ┌──────────────┐
                  │ LLM Filler    │  ← DeepSeek API fills # LLM_FILL: markers
                  │ (Business Logic)│
                  └──────┬───────┘
                         ▼
                  ┌──────────────┐
                  │ Feedback Loop │  ← Run tests → errors → LLM fix → repeat
                  │ (Innovation)  │
                  └──────┬───────┘
                         ▼
                  ┌──────────────┐
                  │ Full App Code │  FastAPI + React + SQLite
                  └──────────────┘
```

### Pure LLM Baseline (for comparison)

```
Natural Language Requirements → DeepSeek API → Complete App Code
```

## Project Structure

```
├── models/                # Domain model definitions (3 sizes)
│   ├── small.yaml         #   3 entities,  3 relationships,  2 business rules
│   ├── medium.yaml        #   6 entities,  6 relationships,  6 business rules
│   └── large.yaml         #  11 entities, 10+ relationships, 10 business rules
├── src/
│   ├── parser/            # YAML model parser (YAML → Pydantic IR)
│   ├── generator/         # Code skeleton generators (Jinja2 templates)
│   │   ├── sql_generator.py    # IR → SQL DDL
│   │   ├── api_generator.py    # IR → FastAPI (routes, models, schemas)
│   │   └── ui_generator.py     # IR → React (pages, API client, routing)
│   ├── llm/               # LLM integration (DeepSeek API)
│   │   ├── client.py           # OpenAI-compatible DeepSeek client
│   │   ├── filler.py           # Model-driven business logic filler
│   │   ├── baseline.py         # Pure LLM full-code generator
│   │   └── prompts.py          # Prompt templates
│   ├── feedback/          # Bidirectional feedback loop (innovation)
│   └── evaluator/         # Automated quality evaluation
│       ├── structure.py        # Structural correctness scoring
│       ├── compilability.py    # Syntax/build check
│       └── consistency.py      # Cross-run output stability
├── templates/             # Jinja2 code templates
│   ├── sql/schema.sql.j2
│   ├── fastapi/{main,models,routes,schemas}.py.j2
│   └── react/{App,ListPage,FormPage,api}.tsx.j2
├── experiments/           # Experiment orchestration
│   ├── run.py             # Batch runner (N runs × 2 methods × 3 model sizes)
│   └── analyze.py         # Results analysis and reporting
├── tests/                 # Test suite
└── .github/workflows/     # CI/CD pipeline
```

## Setup

### Prerequisites

- Python 3.10+
- Conda (recommended) or venv
- DeepSeek API key

### Installation

```bash
# Create and activate conda environment
conda create -n web_code_gen python=3.11
conda activate web_code_gen

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
export DEEPSEEK_API_KEY=your_api_key_here
```

Or create a `.env` file (must be set before running LLM-dependent features).

## Usage

### 1. Generate Code Skeleton (Model-Driven)

```bash
python -c "
from src.parser.parser import parse_model
from src.generator.sql_generator import generate_sql
from src.generator.api_generator import generate_api
from src.generator.ui_generator import generate_ui

model = parse_model('models/small.yaml')
generate_sql(model, 'output/demo/backend')
generate_api(model, 'output/demo/backend')
generate_ui(model, 'output/demo/frontend')
print('Skeleton generated in output/demo/')
"
```

### 2. Fill Business Logic with LLM

```bash
python -c "
from src.parser.parser import parse_model
from src.llm.filler import fill_skeleton

model = parse_model('models/small.yaml')
fill_skeleton(model, 'output/demo/backend')
print('Business logic filled')
"
```

### 3. Run Comparison Experiment

```bash
# Single model, 3 runs per method
python experiments/run.py --model small --runs 3

# All models, 5 runs per method
python experiments/run.py --all --runs 5
```

### 4. Analyze Results

```bash
python experiments/analyze.py experiments/results/experiment_*.json
```

### 5. Run Tests

```bash
# All tests
pytest tests/ -v

# Exclude LLM integration tests (no API key needed)
pytest tests/ -v --ignore=tests/test_baseline.py
```

## Evaluation Metrics

| Metric | Description | Method |
|--------|-------------|--------|
| **Structure Score** | Entity/endpoint/table count match vs. model | Automated parser check |
| **Compilability Score** | Python syntax + import + npm build pass rate | `py_compile` + `npm build` |
| **Consistency Score** | Output similarity across multiple runs | SequenceMatcher diff ratio |
| **Feedback Iterations** | Rounds needed for code to pass all checks | Test-fix-retry loop count |

## Innovation: Bidirectional Feedback Loop

The key innovation is a feedback mechanism that automatically improves generated code:

1. **Generate** → Code skeleton filled by LLM
2. **Test** → Automated syntax check and import validation
3. **Feedback** → Error messages sent back to LLM with model context
4. **Fix** → LLM corrects code within model constraints
5. **Repeat** → Loop until all checks pass (max 3 iterations)

The model context acts as a constraint boundary, preventing the LLM from making structurally incorrect fixes — a key advantage over pure LLM approaches where the entire codebase is mutable.

## Case Study System

The project uses a **Student Course Selection and Management System** as the case study domain, covering:

- User management (students, teachers, admins)
- Course management with departments and programs
- Enrollment with capacity and prerequisite checks
- Grade and assignment management
- Schedule conflict detection

## Tech Stack

- **LLM**: DeepSeek-V4-pro (OpenAI-compatible API)
- **Backend**: Python FastAPI + SQLAlchemy + SQLite
- **Frontend**: React + TypeScript
- **Templates**: Jinja2
- **Validation**: Pydantic
- **Testing**: pytest
- **CI/CD**: GitHub Actions
