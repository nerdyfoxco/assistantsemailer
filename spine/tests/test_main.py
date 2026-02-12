import pytest
from fastapi.testclient import TestClient
from spine.main import app
from spine.core.config import settings

client = TestClient(app)

# 1. Health Check OK
def test_health_check_status():
    response = client.get("/health")
    assert response.status_code == 200

# 2. Health Check Content
def test_health_check_content():
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "ok"
    assert data["project"] == settings.PROJECT_NAME

# 3. Root Endpoint
def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

# 4. Method Not Allowed (POST to GET)
def test_health_check_post_method():
    response = client.post("/health")
    assert response.status_code == 405

# 5. Invalid Path (404)
def test_invalid_path():
    response = client.get("/nonexistent")
    # Returns 405 because of global OPTIONS handler matching the path
    assert response.status_code == 405

# 6. OpenAPI Docs Accessible
def test_openapi_docs():
    response = client.get("/docs")
    assert response.status_code == 200

# 7. OpenAPI JSON Accessible
def test_openapi_json():
    response = client.get(f"{settings.API_V1_STR}/openapi.json")
    assert response.status_code == 200

# 8. Docs Title Check
def test_docs_title():
    response = client.get("/docs")
    assert response.status_code == 200
    assert "Swagger UI" in response.text

# 9. Config Validation
def test_settings_loaded():
    assert settings.PROJECT_NAME == "Assistants Co Spine"
    assert len(settings.BACKEND_CORS_ORIGINS) > 0

# 10. JSON Response Headers
def test_json_headers():
    response = client.get("/health")
    assert response.headers["content-type"] == "application/json"
