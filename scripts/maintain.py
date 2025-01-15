#!/usr/bin/env python
"""Maintenance script to run all code quality tools."""
import argparse
import subprocess
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


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


def format_code() -> bool:
    """Run code formatters."""
    success = True
    success &= run_command(["black", "."], "Black formatter")
    success &= run_command(["isort", "."], "Import sorting")
    return success


def check_quality() -> bool:
    """Run code quality checks."""
    success = True
    success &= run_command(["flake8"], "Flake8 linting")
    success &= run_command(["pylint", "tci"], "Pylint checks")
    success &= run_command(["mypy", "tci"], "Type checking")
    success &= run_command(
        ["bandit", "-c", "pyproject.toml", "-r", "."], "Security checks"
    )
    return success


def run_tests() -> bool:
    """Run tests with coverage."""
    return run_command(
        ["pytest", "--cov=tci", "--cov-report=term-missing", "--cov-report=html"],
        "Tests with coverage",
    )


def build_docs() -> bool:
    """Build documentation."""
    return run_command(["mkdocs", "build"], "Documentation build")


def check_dependencies() -> bool:
    """Check for outdated dependencies."""
    success = True
    success &= run_command(["pip", "list", "--outdated"], "Check outdated dependencies")
    success &= run_command(["pip-audit"], "Security audit of dependencies")
    return success


def clean_artifacts() -> bool:
    """Clean up Python artifacts and cache files."""
    success = True
    # Clean Python cache files
    success &= run_command(
        [
            "find",
            ".",
            "-type",
            "d",
            "-name",
            "__pycache__",
            "-exec",
            "rm",
            "-r",
            "{}",
            "+",
        ],
        "Clean Python cache",
    )
    # Clean test/coverage artifacts
    success &= run_command(
        [
            "rm",
            "-rf",
            ".coverage",
            "htmlcov",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
        ],
        "Clean test artifacts",
    )
    # Clean build artifacts
    success &= run_command(
        ["rm", "-rf", "build/", "dist/", "*.egg-info"], "Clean build artifacts"
    )
    return success


def serve_docs() -> bool:
    """Serve documentation locally."""
    return run_command(["mkdocs", "serve"], "Serve documentation")


def main():
    parser = argparse.ArgumentParser(description="Run maintenance tasks")
    parser.add_argument("--format", action="store_true", help="Format code")
    parser.add_argument("--check", action="store_true", help="Run code quality checks")
    parser.add_argument("--test", action="store_true", help="Run tests")
    parser.add_argument("--docs", action="store_true", help="Build docs")
    parser.add_argument(
        "--serve-docs", action="store_true", help="Serve documentation locally"
    )
    parser.add_argument("--deps", action="store_true", help="Check dependencies")
    parser.add_argument("--clean", action="store_true", help="Clean artifacts")
    parser.add_argument(
        "--all", action="store_true", help="Run all tasks (except serve-docs)"
    )

    args = parser.parse_args()

    # If no args, show help
    if not any(vars(args).values()):
        parser.print_help()
        return

    success = True

    if args.clean:
        success &= clean_artifacts()

    if args.all or args.format:
        success &= format_code()

    if args.all or args.check:
        success &= check_quality()

    if args.all or args.test:
        success &= run_tests()

    if args.all or args.docs:
        success &= build_docs()

    if args.all or args.deps:
        success &= check_dependencies()

    if args.serve_docs:
        success &= serve_docs()

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
