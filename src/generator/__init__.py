from pathlib import Path

from src.generator.engine import render_template
from src.parser.ir import ModelIR


def generate_run_script(model: ModelIR, output_dir: str | Path) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    content = render_template("run.sh.j2", model=model)
    script_path = output_dir / "run.sh"
    script_path.write_text(content, encoding="utf-8")
    script_path.chmod(0o755)
    return script_path
