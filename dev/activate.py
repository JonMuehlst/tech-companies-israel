#!/usr/bin/env python
"""Generate shell commands to activate the environment and set PYTHONPATH."""
import argparse
import platform
import sys
from pathlib import Path
from typing import NoReturn

from dev.utils import get_pythonpath_cmd, load_env_config


def generate_activation_commands() -> Path:
    """Generate shell commands to activate venv and set PYTHONPATH."""
    project_root: Path = Path(__file__).parent.parent
    config = load_env_config()

    venv_path: Path = Path(config["VENV_PATH"])
    is_windows: bool = platform.system() == "Windows"

    if not venv_path.exists():
        print(f"[X] Virtual environment not found: {venv_path}")
        print(f"Run setup first: python dev/setup_env.py")
        sys.exit(1)

    # Determine paths based on OS
    if is_windows:
        activate_script: Path = venv_path / "Scripts" / "Activate.ps1"
        commands: list[str] = [
            "# PowerShell activation script",
            f". {activate_script}",
            get_pythonpath_cmd(project_root, is_windows=True),
            "Write-Host '[OK] Environment activated and PYTHONPATH set!' -ForegroundColor Green",
        ]
        output_file: str = "activate.ps1"
    else:
        activate_script: Path = venv_path / "bin" / "activate"
        commands: list[str] = [
            f"source {activate_script}",
            get_pythonpath_cmd(project_root, is_windows=False),
            "echo '[OK] Environment activated and PYTHONPATH set!'",
        ]
        output_file: str = "activate.sh"

    # Write commands to file
    output_path: Path = project_root / output_file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(commands))

    print(f"\n=== Environment Activation ===")
    if is_windows:
        print(f"Run: . .\\{output_file}")
    else:
        print(f"Run: source {output_file}")

    return output_path


def main() -> NoReturn:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Generate shell script to activate environment and set PYTHONPATH"
    )
    args: argparse.Namespace = parser.parse_args()
    generate_activation_commands()
    sys.exit(0)


if __name__ == "__main__":
    main()
