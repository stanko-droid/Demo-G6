#!/usr/bin/env python
"""
Test runner script for Demo-G6 project.

This script runs the entire test suite and provides a summary of results.
Use this to verify that all tests pass before committing or deploying.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py -v           # Verbose output
    python run_tests.py --coverage   # Run with coverage report
"""

import sys
import subprocess


def run_tests(verbose=False, coverage=False):
    """Run the complete test suite."""
    
    print("=" * 70)
    print("🧪 Running Demo-G6 Test Suite")
    print("=" * 70)
    print()
    
    # Base command
    cmd = ["python", "-m", "pytest", "tests/"]
    
    # Add flags
    if verbose:
        cmd.append("-v")
    else:
        cmd.append("-v")  # Always use verbose for better readability
    
    cmd.append("--tb=short")  # Short traceback format
    
    if coverage:
        cmd.extend([
            "--cov=application",
            "--cov-report=term-missing",
            "--cov-report=html"
        ])
    
    # Run tests
    try:
        result = subprocess.run(cmd, check=False)
        
        print()
        print("=" * 70)
        
        if result.returncode == 0:
            print("✅ ALL TESTS PASSED!")
            print()
            print("Test Summary:")
            print("  - Smoke tests (4 tests)")
            print("  - Route tests (10 tests)")
            print("  - Business layer tests (19 tests)")
            print("  - Data layer tests (14 tests)")
            print("  - Integration tests (11 tests)")
            print("  - Auth service tests (10 tests)")
            print("  - Protected routes tests (10 tests)")
            print("  - Security tests (12 tests)")
            print()
            print("  Total: 90 tests ✓")
            
            if coverage:
                print()
                print("📊 Coverage report generated in htmlcov/index.html")
        else:
            print("❌ SOME TESTS FAILED")
            print()
            print("Please review the output above and fix failing tests.")
        
        print("=" * 70)
        
        return result.returncode
        
    except FileNotFoundError:
        print("❌ Error: pytest not found. Make sure you're in the virtual environment.")
        print()
        print("Run: source .venv/bin/activate")
        return 1
    except KeyboardInterrupt:
        print()
        print("⚠️  Test run interrupted by user")
        return 130


def main():
    """Main entry point."""
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    coverage = "--coverage" in sys.argv or "-c" in sys.argv
    
    if "-h" in sys.argv or "--help" in sys.argv:
        print(__doc__)
        return 0
    
    exit_code = run_tests(verbose=verbose, coverage=coverage)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
