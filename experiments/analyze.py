#!/usr/bin/env python3
"""
Analyze experiment results and generate comparison reports.

Usage:
    python experiments/analyze.py experiments/results/experiment_20260520_120000.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


def load_results(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def compute_summary(results: list[dict]) -> dict:
    """Group results by method+model and compute averages."""
    groups = defaultdict(lambda: defaultdict(list))

    for r in results:
        if "error" in r or "average_similarity" in r:
            continue  # Skip failed runs and consistency entries
        key = (r["method"], r["model"])
        groups[key]["structure"].append(r["structure_score"])
        groups[key]["compilability"].append(r["compilability_score"])
        groups[key]["elapsed"].append(r["elapsed_seconds"])
        if r.get("feedback_iterations", 0) > 0:
            groups[key]["feedback_iters"].append(r["feedback_iterations"])

    summary = {}
    for (method, model), metrics in groups.items():
        summary[f"{method}/{model}"] = {
            "structure_avg": _mean(metrics["structure"]),
            "structure_std": _std(metrics["structure"]),
            "compilability_avg": _mean(metrics["compilability"]),
            "compilability_std": _std(metrics["compilability"]),
            "elapsed_avg": _mean(metrics["elapsed"]),
            "elapsed_std": _std(metrics["elapsed"]),
            "num_runs": len(metrics["structure"]),
        }
        if metrics.get("feedback_iters"):
            summary[f"{method}/{model}"]["feedback_iters_avg"] = _mean(metrics["feedback_iters"])

    return summary


def compute_consistency(results: list[dict]) -> dict:
    """Extract consistency scores."""
    cons = {}
    for r in results:
        if "average_similarity" in r:
            key = f"{r['method']}/{r['model']}"
            cons[key] = {
                "average_similarity": r["average_similarity"],
                "total_files": r["total_files"],
            }
    return cons


def print_report(summary: dict, consistency: dict) -> None:
    print("\n" + "=" * 80)
    print("EXPERIMENT REPORT: Model-Driven vs Pure LLM Code Generation")
    print("=" * 80)

    # Table header
    print(f"\n{'Configuration':<30} {'#Runs':<7} {'Struct':<9} {'Compil':<9} {'Time(s)':<10} {'Consist':<9} {'Feedback':<10}")
    print("-" * 85)

    for config, stats in sorted(summary.items()):
        method_model = config
        n = stats["num_runs"]
        s_avg = stats["structure_avg"]
        c_avg = stats["compilability_avg"]
        t_avg = stats["elapsed_avg"]
        cons_key = config
        cons_val = consistency.get(cons_key, {}).get("average_similarity", "N/A")
        fb_val = stats.get("feedback_iters_avg", "N/A")

        cons_str = f"{cons_val:.3f}" if isinstance(cons_val, (int, float)) else str(cons_val)
        fb_str = f"{fb_val:.1f}" if isinstance(fb_val, (int, float)) else str(fb_val)

        print(f"{method_model:<30} {n:<7} {s_avg:<9.3f} {c_avg:<9.3f} {t_avg:<10.1f} {cons_str:<9} {fb_str:<10}")

    # Model-driven vs Pure LLM comparison
    print(f"\n{'='*80}")
    print("MODEL-DRIVEN vs PURE LLM: Average Scores")
    print(f"{'='*80}")

    for model_size in ["small", "medium", "large"]:
        md_key = f"model_driven/{model_size}"
        pl_key = f"pure_llm/{model_size}"
        if md_key in summary and pl_key in summary:
            md = summary[md_key]
            pl = summary[pl_key]
            struct_diff = md["structure_avg"] - pl["structure_avg"]
            comp_diff = md["compilability_avg"] - pl["compilability_avg"]
            print(f"\n{model_size.upper()} MODEL:")
            print(f"  Structure:     MD={md['structure_avg']:.3f}  LLM={pl['structure_avg']:.3f}  Δ={struct_diff:+.3f}")
            print(f"  Compilability: MD={md['compilability_avg']:.3f}  LLM={pl['compilability_avg']:.3f}  Δ={comp_diff:+.3f}")
            print(f"  Time:          MD={md['elapsed_avg']:.1f}s  LLM={pl['elapsed_avg']:.1f}s")


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _std(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = _mean(values)
    return (sum((v - m) ** 2 for v in values) / (len(values) - 1)) ** 0.5


def main():
    parser = argparse.ArgumentParser(description="Analyze experiment results")
    parser.add_argument("results_file", help="Path to results JSON file")
    args = parser.parse_args()

    results = load_results(args.results_file)
    summary = compute_summary(results)
    consistency = compute_consistency(results)
    print_report(summary, consistency)


if __name__ == "__main__":
    main()
