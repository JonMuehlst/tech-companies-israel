#!/usr/bin/env python
"""Environment setup script for the project."""
import argparse
import platform
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

from dev.utils import get_pythonpath_cmd, load_env_config


def run_command(command: list[str], description: str) -> bool:
    """Run a command and return True if successful."""
    print(f"\n=== Running {description} ===")
    try:
        subprocess.run(command, check=True)
        print(f"✅ {description} passed")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ {description} failed")
        return False


def setup_environment(with_dev: bool = False) -> bool:
    """Setup virtual environment and PYTHONPATH."""
    project_root: Path = Path(__file__).parent.parent
    is_windows: bool = platform.system() == "Windows"

    # Load configuration from env.dev
    config = load_env_config()
    venv_path: Path = Path(config["VENV_PATH"])

    # Create venv if it doesn't exist
    if not venv_path.exists():
        print(f"Creating virtual environment at: {venv_path}")
        if not run_command(
            ["python", "-m", "venv", str(venv_path)], "Create virtualenv"
        ):
            return False

    # Determine activation script and PYTHONPATH command
    if is_windows:
        activate_script: Path = venv_path / "Scripts" / "activate.bat"
        python_path_cmd: str = get_pythonpath_cmd(project_root, is_windows=True)
        pip_path: Path = venv_path / "Scripts" / "pip.exe"
    else:
        activate_script: Path = venv_path / "bin" / "activate"
        python_path_cmd: str = get_pythonpath_cmd(project_root, is_windows=False)
        pip_path: Path = venv_path / "bin" / "pip"

    if not activate_script.exists():
        print(f"❌ Activation script not found: {activate_script}")
        return False

    # Print setup instructions
    print("\n=== Environment Setup Instructions ===")
    print("1. Activate the virtual environment:")
    if is_windows:
        print(f"   call {activate_script}")
    else:
        print(f"   source {activate_script}")

    print("\n2. Set PYTHONPATH:")
    print(f"   {python_path_cmd}")

    # Print dependency installation instructions
    req_file: Path = project_root / "requirements.txt"
    dev_req_file: Path = project_root / "requirements-dev.txt"

    print("\n3. Install dependencies:")
    if req_file.exists():
        print(f"   pip install -r {req_file}")
    if with_dev and dev_req_file.exists():
        print(f"   pip install -r {dev_req_file}")

    # Print verification instructions
    print("\n4. Verify setup:")
    print("   python -c 'import tci; print(\"✅ Environment setup successful!\")'")

    return True


def main() -> NoReturn:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Setup development environment"
    )
    parser.add_argument(
        "--with-dev", action="store_true", help="Include development dependencies"
    )

    args: argparse.Namespace = parser.parse_args()

    if not setup_environment(args.with_dev):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
