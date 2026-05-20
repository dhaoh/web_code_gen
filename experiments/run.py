#!/usr/bin/env python3
"""
Experiment runner: compare model-driven vs pure LLM code generation.

Usage:
    python experiments/run.py --model small --runs 3
    python experiments/run.py --all --runs 5
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Ensure project root in path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.parser.parser import parse_model
from src.generator.sql_generator import generate_sql
from src.generator.api_generator import generate_api
from src.generator.ui_generator import generate_ui
from src.llm.filler import fill_skeleton
from src.llm.baseline import generate_from_description
from src.feedback.loop import run_feedback_loop, FeedbackResult
from src.evaluator.structure import evaluate_structure, StructureScore
from src.evaluator.compilability import evaluate_compilability, CompilabilityScore
from src.evaluator.consistency import evaluate_consistency, ConsistencyScore


PROJECT_ROOT = Path(__file__).parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
OUTPUT_DIR = PROJECT_ROOT / "output"
RESULTS_DIR = PROJECT_ROOT / "experiments" / "results"


def run_single_experiment(
    model_path: Path,
    method: str,
    run_id: int,
) -> dict:
    """Run one generation + evaluation cycle."""
    model = parse_model(model_path)
    model_name = model_path.stem
    run_dir = OUTPUT_DIR / method / model_name / f"run_{run_id}"

    # Clean previous run
    if run_dir.exists():
        shutil.rmtree(run_dir)

    start = time.time()

    try:
        if method == "model_driven":
            # Step 1: Generate skeleton
            backend_dir = run_dir / "backend"
            frontend_dir = run_dir / "frontend"
            generate_sql(model, backend_dir)
            generate_api(model, backend_dir)
            generate_ui(model, frontend_dir)

            # Step 2: LLM fills business logic
            fill_skeleton(model, backend_dir)

            # Step 3: Feedback loop
            feedback: FeedbackResult = run_feedback_loop(model, backend_dir)
            feedback_iterations = feedback.iterations
            feedback_pass = feedback.final_pass

        elif method == "pure_llm":
            # Step 1: Generate everything from NL description
            generate_from_description(model, run_dir)

            # Step 2: No feedback loop by default (pure LLM)
            feedback_iterations = 0
            feedback_pass = None

        else:
            raise ValueError(f"Unknown method: {method}")

        elapsed = time.time() - start

        # Evaluate
        struct = evaluate_structure(model, run_dir)
        comp = evaluate_compilability(run_dir)

        return {
            "method": method,
            "model": model_name,
            "run_id": run_id,
            "elapsed_seconds": round(elapsed, 2),
            "feedback_iterations": feedback_iterations,
            "feedback_pass": feedback_pass,
            "structure_score": round(struct.score, 4),
            "structure_details": struct.details,
            "compilability_score": round(comp.score, 4),
            "compilability_details": {
                "python_syntax_pass": comp.python_syntax_pass,
                "python_import_pass": comp.python_import_pass,
                "frontend_build_pass": comp.frontend_build_pass,
                "has_frontend": comp.has_frontend,
                "errors": comp.errors[:10],
            },
        }

    except Exception as e:
        elapsed = time.time() - start
        return {
            "method": method,
            "model": model_name,
            "run_id": run_id,
            "elapsed_seconds": round(elapsed, 2),
            "error": str(e),
            "structure_score": 0.0,
            "compilability_score": 0.0,
        }


def run_consistency_experiment(
    model_path: Path,
    method: str,
    num_runs: int,
) -> dict:
    """Run multiple generations and compute consistency."""
    run_dirs = []
    for i in range(num_runs):
        run_dir = OUTPUT_DIR / method / model_path.stem / f"run_{i}"
        run_dirs.append(str(run_dir))

    consistency = evaluate_consistency(run_dirs)
    return {
        "method": method,
        "model": model_path.stem,
        "num_runs": num_runs,
        "average_similarity": round(consistency.average_similarity, 4),
        "total_files": consistency.total_files,
        "file_scores": [round(s, 4) for s in consistency.file_similarity_scores],
    }


def main():
    parser = argparse.ArgumentParser(description="Run code generation experiments")
    parser.add_argument("--model", choices=["small", "medium", "large"], help="Model size to test")
    parser.add_argument("--all", action="store_true", help="Test all model sizes")
    parser.add_argument("--runs", type=int, default=3, help="Number of runs per experiment")
    parser.add_argument("--method", choices=["model_driven", "pure_llm", "both"],
                        default="both", help="Which method to test")
    args = parser.parse_args()

    if args.all:
        model_sizes = ["small", "medium", "large"]
    elif args.model:
        model_sizes = [args.model]
    else:
        parser.error("Specify --model or --all")

    methods = ["model_driven", "pure_llm"] if args.method == "both" else [args.method]

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    all_results = []

    for model_size in model_sizes:
        model_path = MODELS_DIR / f"{model_size}.yaml"
        if not model_path.exists():
            print(f"Model not found: {model_path}")
            continue

        for method in methods:
            print(f"\n{'='*60}")
            print(f"Experiment: {method} / {model_size} ({args.runs} runs)")
            print(f"{'='*60}")

            for run_id in range(args.runs):
                print(f"  Run {run_id + 1}/{args.runs}...", end=" ", flush=True)
                result = run_single_experiment(model_path, method, run_id)
                all_results.append(result)
                if "error" in result:
                    print(f"ERROR: {result['error'][:100]}")
                else:
                    print(
                        f"struct={result['structure_score']:.2f} "
                        f"comp={result['compilability_score']:.2f} "
                        f"time={result['elapsed_seconds']}s"
                    )

            # Consistency
            if args.runs >= 2:
                print(f"  Computing consistency...", end=" ", flush=True)
                cons = run_consistency_experiment(model_path, method, args.runs)
                all_results.append(cons)
                print(f"similarity={cons['average_similarity']:.4f}")

    # Save results
    results_file = RESULTS_DIR / f"experiment_{timestamp}.json"
    results_file.write_text(json.dumps(all_results, indent=2), encoding="utf-8")
    print(f"\nResults saved to {results_file}")


if __name__ == "__main__":
    main()
