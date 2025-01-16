# Development Tools

This directory contains tools for development and maintenance of the project.

## Available Tools

### Environment Setup and Activation
```bash
# Initial setup (creates virtual environment)
python dev/setup_env.py venv --with-dev  # Includes development dependencies

# Generate activation script (do this once)
python dev/activate.py venv

# Activate environment (do this every time)
source activate.sh    # On Unix
.\activate.bat       # On Windows
```

### Code Maintenance (`maintain.py`)

The `maintain.py` script provides various commands for code maintenance:

```bash
# Run all maintenance tasks
python dev/maintain.py --all

# Code Formatting
python dev/maintain.py --format    # Runs black and isort

# Quality Checks
python dev/maintain.py --check     # Runs flake8, pylint, mypy, and bandit

# Testing
python dev/maintain.py --test      # Runs pytest with coverage

# Documentation
python dev/maintain.py --docs      # Builds MkDocs documentation
python dev/maintain.py --serve-docs # Serves documentation locally

# Dependencies
python dev/maintain.py --deps      # Checks for outdated dependencies

# Cleanup
python dev/maintain.py --clean     # Removes artifacts and cache files
```

### Environment Files
- `env.dev.example` - Template for development environment variables
- `env.dev` - Your local development environment variables (not committed)

### Utility Modules
- `utils.py` - Common utility functions used by development tools
- `setup_env.py` - Environment setup and dependency management
- `activate.py` - Generates environment activation scripts

## Common Development Tasks

1. Setting up a new development environment:
```bash
# Initial setup
python dev/setup_env.py venv --with-dev

# Generate and run activation script
python dev/activate.py venv
source activate.sh  # or .\activate.bat on Windows

# Run all checks
python dev/maintain.py --all
```

2. Daily development workflow:
```bash
# 1. Activate environment
source activate.sh  # or .\activate.bat on Windows

# 2. Before committing changes
python dev/maintain.py --format --check --test
```

3. Working on documentation:
```bash
# Build and serve docs
python dev/maintain.py --serve-docs
```

4. Cleaning up:
```bash
# Remove all build artifacts and cache
python dev/maintain.py --clean
```

## Notes

- Always activate your environment before running any development commands
- The `--with-dev` flag in setup includes additional dependencies needed for development
- Run `maintain.py --all` before submitting pull requests to ensure all checks pass 