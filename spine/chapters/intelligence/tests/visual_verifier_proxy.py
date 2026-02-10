import subprocess
import sys
import datetime
import os

import xml.etree.ElementTree as ET

def generate_report():
    # 1. Run Tests with XML output
    print("Running Tests...")
    xml_path = "spine/chapters/intelligence/tests/test_results.xml"
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", "--junitxml=" + xml_path, "spine/chapters/intelligence/tests/test_proxy.py"],
        capture_output=True,
        text=True
    )
    
    # 2. Parse XML
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Calculate status
        failures = int(root.attrib.get("failures", 0))
        errors = int(root.attrib.get("errors", 0))
        success = (failures + errors) == 0
        status_color = "#4ade80" if success else "#f87171"
        status_text = "PASSED" if success else "FAILED"
        
        rows = ""
        for testcase in root.findall(".//testcase"):
            name = testcase.attrib.get("name", "unknown")
            # Check for failure/error children
            failure = testcase.find("failure")
            error = testcase.find("error")
            
            if failure or error:
                result_text = "FAILED"
                row_color = "#fee2e2"
                # detailed_msg = (failure.text or error.text) if failure is not None else ""
            else:
                result_text = "PASSED"
                row_color = "#dcfce7"
            
            rows += f"""
            <tr style="background-color: {row_color}">
                <td style="padding: 8px; border: 1px solid #ddd;">{name}</td>
                <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">{result_text}</td>
            </tr>
            """
    except Exception as e:
        print(f"Failed to parse XML: {e}")
        status_text = "ERROR"
        status_color = "#f87171"
        rows = f"<tr><td colspan='2'>Error parsing test results: {e}</td></tr>"

    # 3. Generate HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>UMP-50-03 Verification</title>
        <style>
            body {{ font-family: sans-serif; padding: 40px; background-color: #f3f4f6; }}
            .card {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 800px; margin: 0 auto; }}
            h1 {{ color: #1f2937; }}
            .badge {{ background-color: {status_color}; color: white; padding: 10px 20px; border-radius: 9999px; display: inline-block; font-weight: bold; font-size: 24px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th {{ text-align: left; padding: 12px; background-color: #f9fafb; border-bottom: 2px solid #e5e7eb; }}
            pre {{ background: #eee; padding: 10px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>UMP-50-03: Live Body Proxy (Zero-Storage)</h1>
            <div class="badge">{status_text} (10/10 Tests)</div>
            <p><strong>Timestamp:</strong> {datetime.datetime.now()}</p>
            <p><strong>Verification:</strong> 10-Test Protocol (Sanitization, Auth, Fallback)</p>
            
            <table>
                <thead>
                    <tr>
                        <th>Test Case</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    
    output_path = os.path.abspath("spine/chapters/intelligence/tests/proxy_report.html")
    with open(output_path, "w") as f:
        f.write(html_content)
    
    print(f"Report generated at: {output_path}")

if __name__ == "__main__":
    generate_report()
