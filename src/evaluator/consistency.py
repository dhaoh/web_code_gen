from __future__ import annotations

import difflib
from dataclasses import dataclass, field
from pathlib import Path

from src.evaluator import iter_code_files


@dataclass
class ConsistencyScore:
    file_similarity_scores: list[float] = field(default_factory=list)
    total_files: int = 0
    details: dict = None

    @property
    def average_similarity(self) -> float:
        if not self.file_similarity_scores:
            return 0.0
        return sum(self.file_similarity_scores) / len(self.file_similarity_scores)

    @property
    def score(self) -> float:
        return self.average_similarity


def evaluate_consistency(run_dirs: list[str | Path]) -> ConsistencyScore:
    """Compare multiple output directories for the same method/model combination."""
    if len(run_dirs) < 2:
        return ConsistencyScore(total_files=0, details={"error": "Need at least 2 runs"})

    score = ConsistencyScore()
    dirs = [Path(d) for d in run_dirs]

    # Collect file paths from first dir
    first_files = _list_code_files(dirs[0])
    score.total_files = len(first_files)

    # For each file, compute pairwise similarity
    for rel_path in first_files:
        contents = []
        for d in dirs:
            f = d / rel_path
            if f.exists():
                contents.append(f.read_text(encoding="utf-8", errors="ignore"))
            else:
                contents.append("")

        if len(contents) >= 2:
            similarities = []
            for i in range(len(contents)):
                for j in range(i + 1, len(contents)):
                    if contents[i] and contents[j]:
                        s = difflib.SequenceMatcher(None, contents[i], contents[j]).ratio()
                    else:
                        s = 0.0 if (contents[i] or contents[j]) else 1.0
                    similarities.append(s)
            score.file_similarity_scores.append(
                sum(similarities) / len(similarities) if similarities else 0.0
            )

    return score


def _list_code_files(directory: Path) -> list[str]:
    """List all code files relative to directory, excluding build/install dirs."""
    files = []
    for ext in ["*.py", "*.tsx", "*.ts", "*.sql"]:
        for f in sorted(iter_code_files(directory, ext), key=lambda p: str(p)):
            files.append(str(f.relative_to(directory)))
    return sorted(files)
