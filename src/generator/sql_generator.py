from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

from src.generator.engine import render_template
from src.parser.ir import ModelIR


def generate_sql(model: ModelIR, output_dir: str | Path) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    sql = render_template(
        "sql/schema.sql.j2",
        model=model,
        now=datetime.now(timezone.utc).isoformat(),
    )

    # Clean up extra blank lines
    sql = re.sub(r"\n{3,}", "\n\n", sql)

    output_path = output_dir / "schema.sql"
    output_path.write_text(sql, encoding="utf-8")
    return output_path
