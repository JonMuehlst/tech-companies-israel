#!/usr/bin/env python
"""Environment setup script for the project."""
import argparse
import platform
import subprocess
import sys
from pathlib import Path


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


def setup_environment(venv_name: str, with_dev: bool = False) -> bool:
    """Setup virtual environment and PYTHONPATH."""
    project_root = Path(__file__).parent.parent
    is_windows = platform.system() == "Windows"
    venv_path = project_root / venv_name

    # Create venv if it doesn't exist
    if not venv_path.exists():
        print(f"Creating virtual environment: {venv_name}")
        if not run_command(
            ["python", "-m", "venv", str(venv_path)], "Create virtualenv"
        ):
            return False

    # Determine activation script and PYTHONPATH command
    if is_windows:
        activate_script = venv_path / "Scripts" / "activate.bat"
        python_path_cmd = f"set PYTHONPATH={project_root}"
        pip_path = venv_path / "Scripts" / "pip.exe"
    else:
        activate_script = venv_path / "bin" / "activate"
        python_path_cmd = f"export PYTHONPATH={project_root}"
        pip_path = venv_path / "bin" / "pip"

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
    req_file = project_root / "requirements.txt"
    dev_req_file = project_root / "requirements-dev.txt"

    print("\n3. Install dependencies:")
    if req_file.exists():
        print(f"   pip install -r {req_file}")
    if with_dev and dev_req_file.exists():
        print(f"   pip install -r {dev_req_file}")

    # Print verification instructions
    print("\n4. Verify setup:")
    print("   python -c 'import tci; print(\"✅ Environment setup successful!\")'")

    return True


def main():
    parser = argparse.ArgumentParser(description="Setup development environment")
    parser.add_argument(
        "venv_name", help="Name of the virtual environment to create/use"
    )
    parser.add_argument(
        "--with-dev", action="store_true", help="Include development dependencies"
    )

    args = parser.parse_args()

    if not setup_environment(args.venv_name, args.with_dev):
        sys.exit(1)


if __name__ == "__main__":
    main()
