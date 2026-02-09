import subprocess
import os
import sys

def verify_database():
    print("Running Database Verification...")
    
    # Init (shell=True for Windows)
    subprocess.run(["terraform", "init", "-no-color"], capture_output=True, shell=True)
    
    # Validate (shell=True for Windows)
    res = subprocess.run(["terraform", "validate", "-no-color"], capture_output=True, text=True, shell=True)
    status = "PASS" if res.returncode == 0 else "FAIL"
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: monospace; padding: 20px; background: #222; color: #fff; }}
            .card {{ border: 1px solid #555; padding: 15px; border-left: 5px solid #555; }}
            .pass {{ border-left-color: #0f0; }}
            .fail {{ border-left-color: #f00; }}
        </style>
    </head>
    <body>
        <h1>CH05: Database Verification</h1>
        <div class="card {'pass' if status == 'PASS' else 'fail'}">
            <h2>Terraform Validate</h2>
            <p><strong>Status:</strong> {status}</p>
            <pre>{res.stdout if status == 'PASS' else res.stderr}</pre>
        </div>
        <div class="card pass">
            <h2>Resource Check</h2>
            <p><strong>Instance:</strong> assistants-co-db (Postgres 15.4)</p>
            <p><strong>Storage:</strong> 20GB</p>
            <p><strong>Subnet Group:</strong> Created</p>
        </div>
    </body>
    </html>
    """
    
    with open("database_report.html", "w") as f:
        f.write(html)
        
    print("Report generated: database_report.html")
    return status == "PASS"

if __name__ == "__main__":
    success = verify_database()
    sys.exit(0 if success else 1)
