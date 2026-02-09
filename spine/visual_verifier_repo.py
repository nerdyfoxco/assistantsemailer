import asyncio
import subprocess
import sys
from spine.db.database import AsyncSessionLocal
from sqlalchemy import text

def run_repo_tests():
    print("Running Repository Tests (Pytest)...")
    # Using pytest-asyncio
    result = subprocess.run([sys.executable, "-m", "pytest", "spine/tests/test_repository.py"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
    return result.returncode == 0, result.stdout

def generate_report(test_passed, test_output):
    status = "PASS" if test_passed else "FAIL"
    color = "green" if status == "PASS" else "red"
    
    html = f"""
    <html>
    <head>
        <title>UMP-20-03 Verification</title>
        <style>
            body {{ font-family: sans-serif; background: #222; color: #eee; padding: 20px; }}
            .card {{ background: #333; padding: 20px; margin-bottom: 20px; border-left: 5px solid {color}; }}
            h1 {{ color: {color}; }}
            pre {{ background: #111; padding: 10px; overflow: auto; }}
        </style>
    </head>
    <body>
        <h1>UMP-20-03: Repository Layer - {status}</h1>
        
        <div class="card">
            <h2>1. Repository Integration Tests</h2>
            <p>Status: {'PASS' if test_passed else 'FAIL'}</p>
            <details>
                <summary>View Output</summary>
                <pre>{test_output}</pre>
            </details>
        </div>
    </body>
    </html>
    """
    with open("spine/repo_report.html", "w") as f:
        f.write(html)
    print("Report generated: spine/repo_report.html")

async def main():
    test_passed, test_output = run_repo_tests()
    generate_report(test_passed, test_output)
    
    if test_passed:
        print("VERIFICATION SUCCESS")
        sys.exit(0)
    else:
        print("VERIFICATION FAILURE")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
