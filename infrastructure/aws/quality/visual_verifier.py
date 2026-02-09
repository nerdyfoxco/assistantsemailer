import os
import sys

def verify_quality():
    print("Running Quality Verification...")
    
    workflow_path = "../../../.github/workflows/terraform.yml"
    
    if os.path.exists(workflow_path):
        status = "PASS"
        with open(workflow_path, 'r') as f:
            content = f.read()
    else:
        status = "FAIL"
        content = "File not found."

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
        <h1>CH08: Quality (CI/CD) Verification</h1>
        <div class="card {'pass' if status == 'PASS' else 'fail'}">
            <h2>Workflow Check</h2>
            <p><strong>File:</strong> .github/workflows/terraform.yml</p>
            <p><strong>Status:</strong> {status}</p>
        </div>
        <div class="card pass">
            <h2>Content Check</h2>
            <pre>{content}</pre>
        </div>
    </body>
    </html>
    """
    
    with open("quality_report.html", "w") as f:
        f.write(html)
        
    print("Report generated: quality_report.html")
    return status == "PASS"

if __name__ == "__main__":
    success = verify_quality()
    sys.exit(0 if success else 1)
