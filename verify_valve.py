
import asyncio
from unittest.mock import MagicMock
from spine.chapters.action.valve import Valve

async def verify_valve():
    """
    Visual Verification Script for Valve.
    Generates an HTML report showing Allowed vs Blocked attempts.
    """
    # 1. Setup Mock Service
    mock_service = MagicMock()
    mock_service.users.return_value.messages.return_value.send.return_value.execute.return_value = {"id": "SENT_ID_123"}
    builder = MagicMock(return_value=mock_service)
    
    # 2. Setup Valve with Whitelist
    valve = Valve(builder, dev_mode_whitelist=["allowed.com"])
    
    # 3. HTML Builder
    html = """
    <html>
    <body style="font-family: sans-serif; padding: 20px;">
        <h1>Valve Verification (UMP-60-02)</h1>
        <table border="1" cellpadding="10" style="border-collapse: collapse;">
            <tr><th>Test Case</th><th>To Address</th><th>Expected</th><th>Actual Result</th><th>Status</th></tr>
    """
    
    # 4. Test Case A: Allowed Domain
    res_a = await valve.send_email("u1", "c", "raw", "friend@allowed.com")
    status_a = "PASS" if res_a else "FAIL"
    color_a = "green" if res_a else "red"
    
    html += f"""
            <tr>
                <td>Whitelist Allowed</td>
                <td>friend@allowed.com</td>
                <td>True (Sent)</td>
                <td>{res_a}</td>
                <td style="color: {color_a}; font-weight: bold;">{status_a}</td>
            </tr>
    """

    # 5. Test Case B: Blocked Domain
    res_b = await valve.send_email("u1", "c", "raw", "hacker@blocked.com")
    status_b = "PASS" if not res_b else "FAIL" # Expect False
    color_b = "green" if not res_b else "red"
    
    html += f"""
            <tr>
                <td>Whitelist Blocked</td>
                <td>hacker@blocked.com</td>
                <td>False (Blocked)</td>
                <td>{res_b}</td>
                <td style="color: {color_b}; font-weight: bold;">{status_b}</td>
            </tr>
    """

    html += "</table></body></html>"
    
    with open("verify_valve.html", "w") as f:
        f.write(html)
        
    print("Verification HTML generated: verify_valve.html")

if __name__ == "__main__":
    asyncio.run(verify_valve())
