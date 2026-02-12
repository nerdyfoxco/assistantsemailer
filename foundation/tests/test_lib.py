import pytest
import json
import logging
from io import StringIO
from foundation.lib.logging import StructuredLogger, JsonFormatter
from foundation.lib.security import PasswordManager

# Security Tests
def test_password_hashing():
    pwd = "securepassword"
    hashed = PasswordManager.get_password_hash(pwd)
    
    assert hashed != pwd
    assert PasswordManager.verify_password(pwd, hashed) is True
    assert PasswordManager.verify_password("wrong", hashed) is False

# Logging Tests
def test_json_formatting():
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test", level=logging.INFO, pathname="", lineno=0,
        msg="Hello World", args=(), exc_info=None
    )
    output = formatter.format(record)
    data = json.loads(output)
    
    assert data["message"] == "Hello World"
    assert data["level"] == "INFO"
    assert "timestamp" in data

def test_structured_logger_output(capsys):
    # Hack to capture output from standard logging stream
    # Actually, easiest way is to mock the handler or inspect the record
    # But let's rely on capsys capturing stdout if StreamHandler uses sys.stdout (default is stderr)
    
    # Let's force it to stdout for test or mock the handler.
    # We'll just verify the call mechanics.
    
    logger = StructuredLogger("test")
    # Add a memory handler for verification
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonFormatter())
    logger._logger.addHandler(handler)
    
    logger.info("Test Message", tenant_id="t1")
    
    output = stream.getvalue()
    data = json.loads(output)
    
    assert data["message"] == "Test Message"
    assert data["tenant_id"] == "t1"
