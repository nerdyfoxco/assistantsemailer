import subprocess
import sys
import json
import os
import shutil

def check_command(cmd, args):
    try:
        res = subprocess.run([cmd] + args, capture_output=True, text=True, timeout=5)
        if res.returncode == 0:
            return {"status": "OK", "version": res.stdout.strip().split('\n')[0]}
        return {"status": "FAIL", "error": res.stderr.strip()}
    except FileNotFoundError:
        return {"status": "MISSING", "error": "Command not found"}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}

def generate_report():
    checks = {
        "Python": check_command("python", ["--version"]),
        "Node": check_command("node", ["-v"]),
        "Docker": check_command("docker", ["--version"]),
        "Terraform": check_command("terraform", ["--version"]),
        "AWS CLI": check_command("aws", ["--version"]),
        "Git": check_command("git", ["--version"])
    }

    # Generate JSON
    with open("env_status.json", "w") as f:
        json.dump(checks, f, indent=2)

    # Generate HTML
    html = """
    <html>
    <head>
        <style>
            body { font-family: monospace; padding: 20px; background: #1e1e1e; color: #fff; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 10px; border: 1px solid #444; text-align: left; }
            .OK { color: #00ff00; font-weight: bold; }
            .FAIL, .MISSING, .ERROR { color: #ff0000; font-weight: bold; }
            h1 { color: #aaa; }
        </style>
    </head>
    <body>
        <h1>UMP-01-01: Environment Readiness</h1>
        <table>
            <tr><th>Tool</th><th>Status</th><th>Version / Error</th></tr>
    """
    
    all_passed = True
    for tool, result in checks.items():
        css_class = result["status"]
        if css_class != "OK":
            all_passed = False
        html += f"<tr><td>{tool}</td><td class='{css_class}'>{result['status']}</td><td>{result.get('version', result.get('error', ''))}</td></tr>"

    html += """
        </table>
        <br>
        <div id="final-verdict">
    """
    if all_passed: 
        html += "<h2 class='OK'>VERDICT: READY</h2>"
    else:
        html += "<h2 class='FAIL'>VERDICT: NOT READY</h2>"
    
    html += "</div></body></html>"

    with open("env_report.html", "w") as f:
        f.write(html)
        
    print("Environment check complete. Report generated.")
    return all_passed

if __name__ == "__main__":
    success = generate_report()
    sys.exit(0 if success else 1)
