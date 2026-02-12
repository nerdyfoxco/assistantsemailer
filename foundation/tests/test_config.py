import pytest
from foundation.config.settings import GlobalSettings
import os

def test_default_settings():
    settings = GlobalSettings()
    assert settings.ENV == "dev"
    assert settings.PROJECT_NAME == "assistants-co-system"

def test_env_override(monkeypatch):
    monkeypatch.setenv("PROJECT_NAME", "Overridden Project")
    settings = GlobalSettings()
    assert settings.PROJECT_NAME == "Overridden Project"

def test_type_validation_fail(monkeypatch):
    monkeypatch.setenv("ENABLE_AUTHORITY_CHECKS", "not_a_bool")
    with pytest.raises(Exception): # Pydantic ValidationError
         GlobalSettings()

def test_case_insensitive(monkeypatch):
    monkeypatch.setenv("project_name", "Case Insensitive Success")
    settings = GlobalSettings()
    assert settings.PROJECT_NAME == "Case Insensitive Success"
