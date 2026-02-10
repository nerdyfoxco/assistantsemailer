import subprocess
import sys

def run_tests():
    print("Running 10-Test Protocol for Triage...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", "spine/chapters/intelligence/tests/test_triage.py"],
        capture_output=True,
        text=True
    )
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())
