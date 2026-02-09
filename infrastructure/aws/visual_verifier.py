import subprocess
import os
import sys

def verify_terraform():
    print("Running Terraform Verification...")
    
    # 1. Init
    res_init = subprocess.run(["terraform", "init", "-no-color"], capture_output=True, text=True)
    if res_init.returncode != 0:
        print("Terraform Init Failed")
        print(res_init.stderr)
        return False

    # 2. Validate
    res_val = subprocess.run(["terraform", "validate", "-no-color"], capture_output=True, text=True)
    val_status = "PASS" if res_val.returncode == 0 else "FAIL"
    val_msg = res_val.stdout if res_val.returncode == 0 else res_val.stderr
    
    # Generate HTML Report
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: monospace; padding: 20px; background: #1e1e1e; color: #fff; }}
            .card {{ border: 1px solid #444; padding: 15px; margin: 10px 0; border-left: 5px solid #555; }}
            .pass {{ border-left-color: #0f0; }}
            .fail {{ border-left-color: #f00; }}
        </style>
    </head>
    <body>
        <h1>Terraform Verification (CH01)</h1>
        <div class="card {'pass' if val_status == 'PASS' else 'fail'}">
            <h2>Terraform Validate</h2>
            <p><strong>Status:</strong> {val_status}</p>
            <pre>{val_msg}</pre>
        </div>
    </body>
    </html>
    """
    
    with open("plan_report.html", "w") as f:
        f.write(html)
    
    print("Report generated: plan_report.html")
    return val_status == "PASS"

if __name__ == "__main__":
    success = verify_terraform()
    sys.exit(0 if success else 1)
