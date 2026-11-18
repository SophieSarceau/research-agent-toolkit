"""Record how a run was produced next to its outputs."""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent


def _git(*args: str) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", *args], cwd=REPOSITORY_ROOT, capture_output=True, text=True, check=True
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def write_run_record(output_dir: Path) -> None:
    """Write the command, Git commit and uncommitted-change flag to output_dir/run.json."""
    status = _git("status", "--porcelain", "--untracked-files=no")
    record = {
        "command": sys.argv,
        "commit": _git("rev-parse", "HEAD"),
        "uncommitted_changes": None if status is None else bool(status),
        "started_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "run.json").write_text(json.dumps(record, indent=2) + "\n")
