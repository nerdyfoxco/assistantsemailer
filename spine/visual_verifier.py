import subprocess
import time
import sys
import os
import requests
import signal

def run_tests():
    print("Running 10-Test Suite (Pytest)...")
    result = subprocess.run([sys.executable, "-m", "pytest", "spine/tests"], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    return result.returncode == 0, result.stdout

def start_server():
    print("Starting FastAPI Server...")
    # Start uvicorn in background
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "spine.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return proc

def verify_health():
    url = "http://127.0.0.1:8000/health"
    print(f"Checking {url}...")
    for i in range(10):
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                print(f"Health Check Passed: {resp.json()}")
                return True, resp.json()
        except Exception:
            time.sleep(1)
    return False, None

def generate_report(test_passed, test_output, health_passed, health_data):
    status = "PASS" if (test_passed and health_passed) else "FAIL"
    color = "green" if status == "PASS" else "red"
    
    html = f"""
    <html>
    <head>
        <title>UMP-20-01 Verification</title>
        <style>
            body {{ font-family: sans-serif; background: #222; color: #eee; padding: 20px; }}
            .card {{ background: #333; padding: 20px; margin-bottom: 20px; border-left: 5px solid {color}; }}
            h1 {{ color: {color}; }}
            pre {{ background: #111; padding: 10px; overflow: auto; }}
        </style>
    </head>
    <body>
        <h1>UMP-20-01: Backend Skeleton - {status}</h1>
        
        <div class="card">
            <h2>1. Unit Tests (Pytest)</h2>
            <p>Status: {'PASS' if test_passed else 'FAIL'}</p>
            <details>
                <summary>View Output</summary>
                <pre>{test_output}</pre>
            </details>
        </div>
        
        <div class="card">
            <h2>2. Live Health Check</h2>
            <p>Status: {'PASS' if health_passed else 'FAIL'}</p>
            <pre>{health_data}</pre>
        </div>
    </body>
    </html>
    """
    with open("spine/backend_report.html", "w") as f:
        f.write(html)
    print("Report generated: spine/backend_report.html")

def main():
    # 1. Tests
    test_passed, test_output = run_tests()
    
    # 2. Server
    server_proc = start_server()
    time.sleep(3) # warmup
    
    try:
        # 3. Health
        health_passed, health_data = verify_health()
        
        # 4. Report
        generate_report(test_passed, test_output, health_passed, health_data)
        
        if test_passed and health_passed:
            print("VERIFICATION SUCCESS")
            sys.exit(0)
        else:
            print("VERIFICATION FAILURE")
            sys.exit(1)
            
    finally:
        server_proc.terminate()

if __name__ == "__main__":
    main()
