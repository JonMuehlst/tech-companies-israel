"""Shared utilities for development tools."""

import os
import sys
from pathlib import Path
from typing import Dict


def load_env_config() -> Dict[str, str]:
    """Load environment configuration from env.dev file."""
    config: Dict[str, str] = {}
    config_path: Path = Path(__file__).parent / "env.dev"

    if not config_path.exists():
        print(f"[X] Configuration file not found: {config_path}")
        sys.exit(1)

    with open(config_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                # Remove quotes if present
                config[key.strip()] = value.strip().strip('"')

    return config


def get_pythonpath_cmd(project_root: Path, is_windows: bool) -> str:
    """Generate PYTHONPATH command preserving existing path."""
    # Get current PYTHONPATH or empty string if not set
    current_pythonpath = os.environ.get("PYTHONPATH", "")

    # Add project root to PYTHONPATH
    paths = [str(project_root)]
    if current_pythonpath:
        paths.append(current_pythonpath)

    # Join paths using OS-specific separator
    path_sep = ";" if is_windows else ":"
    new_pythonpath = path_sep.join(paths)

    # Return OS-specific command
    if is_windows:
        # PowerShell syntax for setting environment variables
        return f"$env:PYTHONPATH = '{new_pythonpath}'"
    return f"export PYTHONPATH={new_pythonpath}"
