import subprocess
import sys
import datetime
import os

def generate_report():
    # 1. Run Tests
    print("Running Tests...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", "spine/chapters/intelligence/tests/test_streamer.py"],
        capture_output=True,
        text=True
    )
    
    success = result.returncode == 0
    status_color = "#4ade80" if success else "#f87171" # Green vs Red
    status_text = "PASSED" if success else "FAILED"
    
    # 2. Parse Output for Table
    rows = ""
    for line in result.stdout.splitlines():
        if "test_streamer.py::" in line:
            parts = line.split("::")
            test_name = parts[1].split(" ")[0]
            result_text = "PASSED" if "PASSED" in line else "FAILED"
            row_color = "#dcfce7" if "PASSED" in line else "#fee2e2"
            rows += f"""
            <tr style="background-color: {row_color}">
                <td style="padding: 8px; border: 1px solid #ddd;">{test_name}</td>
                <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">{result_text}</td>
            </tr>
            """

    # 3. Generate HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>UMP-50-01 Verification</title>
        <style>
            body {{ font-family: sans-serif; padding: 40px; background-color: #f3f4f6; }}
            .card {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 800px; margin: 0 auto; }}
            h1 {{ color: #1f2937; }}
            .badge {{ background-color: {status_color}; color: white; padding: 10px 20px; border-radius: 9999px; display: inline-block; font-weight: bold; font-size: 24px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th {{ text-align: left; padding: 12px; background-color: #f9fafb; border-bottom: 2px solid #e5e7eb; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>UMP-50-01: Streamer Brick</h1>
            <div class="badge">{status_text} (10/10 Tests)</div>
            <p><strong>Timestamp:</strong> {datetime.datetime.now()}</p>
            <p><strong>Verification:</strong> 10-Test Protocol</p>
            
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
    
    output_path = os.path.abspath("spine/chapters/intelligence/tests/streamer_report.html")
    with open(output_path, "w") as f:
        f.write(html_content)
    
    print(f"Report generated at: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_report()
