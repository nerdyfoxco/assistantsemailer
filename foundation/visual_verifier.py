import json
import sys
import os
import datetime

# Add root to path so we can import foundation modules
sys.path.append(os.getcwd())

from foundation.identity.models import User, Tenant, Resource
from foundation.identity.access import validate_access, TenantMismatchError
from foundation.audit.chain import AuditLedger
from foundation.verification.engine import verify, G_Deny, VerificationFault
from foundation.contracts.validate_drc import validate_drc

def run_visual_verification():
    print("Running Foundation Visual Verification...")
    
    results = {}

    # 1. DRC Check
    drc_path = "foundation/contracts/deployment_readiness.json"
    drc_valid = validate_drc(drc_path)
    with open(drc_path, 'r') as f:
        drc_content = json.load(f)
    results["DRC"] = {
        "status": "PASS" if drc_valid else "FAIL",
        "id": drc_content["deployment_id"],
        "authority_lock": drc_content["security_floor"]["user_final_authority_lock"]
    }

    # 2. Identity Check
    t1 = Tenant(name="Visual Tenant")
    u1 = User(email="visual@test.com", tenant_id=t1.id, role="OWNER")
    r1 = Resource(id="res_1", tenant_id=t1.id)
    r2 = Resource(id="res_2", tenant_id="other_tenant")
    
    try:
        validate_access(u1, r1)
        access_1 = "ALLOWED"
    except Exception as e:
        access_1 = f"ERROR: {e}"

    try:
        validate_access(u1, r2)
        access_2 = "ALLOWED_INCORRECTLY"
    except TenantMismatchError:
        access_2 = "BLOCKED (CORRECT)"
    except Exception as e:
        access_2 = f"ERROR: {e}"

    results["Identity"] = {
        "tenant": t1.name,
        "user": u1.email,
        "same_tenant_access": access_1,
        "cross_tenant_access": access_2
    }

    # 3. Audit Check
    ledger = AuditLedger()
    e1 = ledger.log_event(u1.id, "LOGIN", "system")
    e2 = ledger.log_event(u1.id, "VIEW", r1.id)
    chain_valid = ledger.validate_chain()
    
    results["Audit"] = {
        "chain_length": len(ledger.chain),
        "last_hash": e2.hash[:16] + "...",
        "tamper_check": "PASS" if chain_valid else "FAIL"
    }

    # 4. 15.H Check
    @verify([G_Deny])
    def bad_op(): return "FAIL"

    try:
        bad_op()
        verify_status = "FAIL (Did not block)"
    except VerificationFault:
        verify_status = "PASS (Blocked via G_Deny)"

    results["Phase15H"] = {
        "status": verify_status
    }

    # Generate HTML Report
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: sans-serif; padding: 20px; background: #222; color: #ddd; }}
            .card {{ background: #333; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 5px solid #555; }}
            .pass {{ border-left-color: #0f0; }}
            .fail {{ border-left-color: #f00; }}
            h2 {{ margin-top: 0; }}
            pre {{ background: #111; padding: 10px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <h1>Foundation Visual Verification</h1>
        <p>Generated: {datetime.datetime.now()}</p>

        <div class="card {'pass' if results['DRC']['status'] == 'PASS' else 'fail'}">
            <h2>1. Authority (DRC)</h2>
            <p><strong>Status:</strong> {results['DRC']['status']}</p>
            <p><strong>Deployment ID:</strong> {results['DRC']['id']}</p>
            <p><strong>Authority Lock:</strong> {results['DRC']['authority_lock']}</p>
        </div>

        <div class="card {'pass' if results['Identity']['cross_tenant_access'] == 'BLOCKED (CORRECT)' else 'fail'}">
            <h2>2. Identity (Tenancy)</h2>
            <p><strong>Tenant:</strong> {results['Identity']['tenant']}</p>
            <p><strong>User:</strong> {results['Identity']['user']}</p>
            <p><strong>Same Tenant Access:</strong> {results['Identity']['same_tenant_access']}</p>
            <p><strong>Cross Tenant Access:</strong> {results['Identity']['cross_tenant_access']}</p>
        </div>

        <div class="card {'pass' if results['Audit']['tamper_check'] == 'PASS' else 'fail'}">
            <h2>3. Audit (Ledger)</h2>
            <p><strong>Chain Length:</strong> {results['Audit']['chain_length']}</p>
            <p><strong>Last Hash:</strong> {results['Audit']['last_hash']}</p>
            <p><strong>Integrity Check:</strong> {results['Audit']['tamper_check']}</p>
        </div>

        <div class="card {'pass' if 'PASS' in results['Phase15H']['status'] else 'fail'}">
            <h2>4. Runtime Engine (15.H)</h2>
            <p><strong>G_Deny Test:</strong> {results['Phase15H']['status']}</p>
        </div>
    </body>
    </html>
    """

    with open("foundation_report.html", "w") as f:
        f.write(html)
    
    print("Report generated: foundation_report.html")

if __name__ == "__main__":
    run_visual_verification()
