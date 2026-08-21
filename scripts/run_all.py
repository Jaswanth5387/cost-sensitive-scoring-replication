from __future__ import annotations

import os
import subprocess
import sys

COMMANDS = [
    ["python", "scripts/download_data.py"],
    ["python", "experiments/threshold_sweep.py"],
    ["python", "experiments/error_analysis.py"],
    ["python", "experiments/sensitivity_analysis.py"],
    ["python", "experiments/multi_seed.py"],
    ["python", "experiments/plots.py"],
    ["pytest"],
    ["ruff", "check", "."],
]


def main() -> None:
    os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
    for command in COMMANDS:
        print("+", " ".join(command), flush=True)
        subprocess.run(command, check=True)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        raise SystemExit(error.returncode) from error
    except KeyboardInterrupt:
        sys.exit(130)
