import os
import sys
import subprocess
import webbrowser
from pathlib import Path


def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"Errors: {result.stderr}")
    return result.returncode


def main():
    print("=" * 60)
    print("Generating Test Coverage Report")
    print("=" * 60)

    Path("htmlcov").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)

    print("\n1. Running tests with coverage...")
    cmd = "pytest --cov=src --cov-report=html --cov-report=term-missing tests/"
    if run_command(cmd) != 0:
        print("Error running tests")
        sys.exit(1)

    print("\n2. Generating coverage report...")
    cmd = "coverage html -d htmlcov"
    if run_command(cmd) != 0:
        print("Error generating coverage report")
        sys.exit(1)

    print("\n3. Coverage summary:")
    cmd = "coverage report"
    run_command(cmd)

    report_path = os.path.abspath("htmlcov/index.html")
    print(f"\n4. Report generated at: {report_path}")

    if input("\nOpen report in browser? (y/n): ").lower() == 'y':
        webbrowser.open(f"file://{report_path}")

    print("\n" + "=" * 60)
    print("To view the report manually:")
    print(f"  Open: {report_path}")
    print("Or run: python -m http.server 8000")
    print("Then visit: http://localhost:8000/htmlcov/")
    print("=" * 60)


if __name__ == "__main__":
    main()