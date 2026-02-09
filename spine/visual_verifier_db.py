import asyncio
import subprocess
import sys
import os
from sqlalchemy import select, text
from spine.db.database import AsyncSessionLocal
from spine.db.models import User

def run_tests():
    print("Running DB Unit Tests (Pytest)...")
    # Using pytest-asyncio
    result = subprocess.run([sys.executable, "-m", "pytest", "spine/tests/test_db.py"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
    return result.returncode == 0, result.stdout

async def verify_db_connectivity():
    print("Verifying DB Connectivity...")
    try:
        async with AsyncSessionLocal() as session:
            # Check simple query
            result = await session.execute(text("SELECT 1"))
            val = result.scalar()
            if val == 1:
                print("DB Connection: OK")
                return True
            else:
                print(f"DB Connection Failed: Unexpected value {val}")
                return False
    except Exception as e:
        print(f"DB Connection Error: {e}")
        return False

def generate_report(test_passed, test_output, db_passed):
    status = "PASS" if (test_passed and db_passed) else "FAIL"
    color = "green" if status == "PASS" else "red"
    
    html = f"""
    <html>
    <head>
        <title>UMP-20-02 Verification</title>
        <style>
            body {{ font-family: sans-serif; background: #222; color: #eee; padding: 20px; }}
            .card {{ background: #333; padding: 20px; margin-bottom: 20px; border-left: 5px solid {color}; }}
            h1 {{ color: {color}; }}
            pre {{ background: #111; padding: 10px; overflow: auto; }}
        </style>
    </head>
    <body>
        <h1>UMP-20-02: Database Models - {status}</h1>
        
        <div class="card">
            <h2>1. DB Unit Tests (CRUD)</h2>
            <p>Status: {'PASS' if test_passed else 'FAIL'}</p>
            <details>
                <summary>View Output</summary>
                <pre>{test_output}</pre>
            </details>
        </div>
        
        <div class="card">
            <h2>2. Connectivity Check</h2>
            <p>Status: {'PASS' if db_passed else 'FAIL'}</p>
            <p>Executed: SELECT 1</p>
            <p>Driver: sqlite+aiosqlite</p>
        </div>
    </body>
    </html>
    """
    with open("spine/db_report.html", "w") as f:
        f.write(html)
    print("Report generated: spine/db_report.html")

async def main():
    # 1. Tests
    test_passed, test_output = run_tests()
    
    # 2. Connectivity
    db_passed = await verify_db_connectivity()
    
    # 3. Report
    generate_report(test_passed, test_output, db_passed)
    
    if test_passed and db_passed:
        print("VERIFICATION SUCCESS")
        sys.exit(0)
    else:
        print("VERIFICATION FAILURE")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
