# Development Tools

This directory contains tools for development and maintenance of the project.

## Available Tools

### Environment Setup and Activation
```bash
# Initial setup
python dev/setup_env.py venv --with-dev

# Generate activation script (do this once)
python dev/activate.py venv

# Activate environment (do this every time)
source activate.sh  # On Unix
.\activate.bat     # On Windows
```

### Code Maintenance
```bash
# Run all maintenance tasks
python dev/maintain.py --all

# Format code only
python dev/maintain.py --format

# Run quality checks
python dev/maintain.py --check

# Run tests
python dev/maintain.py --test

# Build documentation
python dev/maintain.py --docs

# Serve documentation locally
python dev/maintain.py --serve-docs

# Check dependencies
python dev/maintain.py --deps

# Clean artifacts
python dev/maintain.py --clean
```

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
python dev/maintain.py --serve-docs
```

4. Cleaning up:
```bash
python dev/maintain.py --clean
``` 