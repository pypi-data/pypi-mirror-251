"""
Main entry point.
"""

import sys
import subprocess

from pathlib import Path
from isolated_environment import isolated_environment

HERE = Path(__file__).parent
TARGET_PY = HERE / "run_isolated.py"
VENV_PATH = Path(HERE) / ".gptneox20b-venv"

REQUIRED_PACKAGES = [
    "transformers",
    "sentencepiece",
    "accelerate",
    "safetensors",
]


def main() -> int:
    env = isolated_environment(VENV_PATH, REQUIRED_PACKAGES)
    cmds_list = ["python", str(TARGET_PY)] + sys.argv[1:]
    rtn = subprocess.call(cmds_list, env=env, shell=True)
    return rtn


if __name__ == "__main__":
    sys.exit(main())
