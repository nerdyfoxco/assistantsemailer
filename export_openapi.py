
import sys
import os
import json
from fastapi.testclient import TestClient

# Add project root to sys.path
sys.path.append(os.getcwd())

try:
    from spine.main import app
    
    openapi_data = app.openapi()
    
    output_path = "docs/openapi-baseline.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(openapi_data, f, indent=2)
        
    print(f"OpenAPI schema exported to {output_path}")
    
except Exception as e:
    print(f"Error exporting OpenAPI: {e}")
    sys.exit(1)
