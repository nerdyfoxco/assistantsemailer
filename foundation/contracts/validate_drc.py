import json
import sys
import os

def validate_drc(file_path):
    print(f"Validating {file_path}...")
    
    if not os.path.exists(file_path):
        print("ERROR: File not found.")
        return False

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON. {e}")
        return False

    # Schema Validation (Manual for now, can use jsonschema lib later if we add it to env)
    required_keys = [
        "contract_version", "deployment_id", "required_capabilities", 
        "security_floor", "exit_condition"
    ]
    
    missing = [k for k in required_keys if k not in data]
    if missing:
        print(f"ERROR: Missing keys: {missing}")
        return False

    # Logic Checks
    if not data["security_floor"].get("no_autonomous_send"):
        print("ERROR: Security Floor violation. 'no_autonomous_send' must be true.")
        return False

    if not data["security_floor"].get("user_final_authority_lock"):
        print("ERROR: Authority violation. 'user_final_authority_lock' must be true.")
        return False

    print("SUCCESS: DRC is valid and compliant with v0 constraints.")
    return True

if __name__ == "__main__":
    success = validate_drc("deployment_readiness.json")
    sys.exit(0 if success else 1)
