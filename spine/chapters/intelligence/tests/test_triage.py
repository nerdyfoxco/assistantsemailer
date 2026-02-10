import pytest
from datetime import datetime
from spine.chapters.intelligence.triage import triage_thread, TriageResult, ConfidenceBand, WorkItemState

# Fixtures
@pytest.fixture
def base_thread():
    return {
        "id": "t1",
        "messages": [
            {
                "id": "m1",
                "internalDate": "1609459200000", # 2021-01-01
                "snippet": "Hello world",
                "payload": {
                    "headers": [
                        {"name": "Subject", "value": "Meeting Request"},
                        {"name": "From", "value": "alice@example.com"}
                    ]
                }
            }
        ]
    }

# 1. Urgent Keyword Detection
def test_triage_urgent_keyword(base_thread):
    base_thread["messages"][0]["payload"]["headers"][0]["value"] = "URGENT: Server Down"
    result = triage_thread(base_thread)
    assert result.confidence == ConfidenceBand.HIGH
    assert "urgent" in result.tags

# 2. Empty Subject Handling
def test_triage_empty_subject(base_thread):
    # Remove subject header
    base_thread["messages"][0]["payload"]["headers"] = [{"name": "From", "value": "me"}]
    result = triage_thread(base_thread)
    assert result.subject == "(No Subject)"
    # Should default to medium/needs_reply if not spam/urgent
    assert result.suggested_state == WorkItemState.NEEDS_REPLY

# 3. VIP Sender Priority
def test_triage_vip_sender(base_thread):
    base_thread["messages"][0]["payload"]["headers"][1]["value"] = "boss@vip.com"
    result = triage_thread(base_thread)
    assert result.is_vip is True
    assert result.confidence == ConfidenceBand.HIGH
    assert "vip" in result.tags

# 4. Spam Detection
def test_triage_spam_detection(base_thread):
    base_thread["messages"][0]["payload"]["headers"][0]["value"] = "You WON the Lottery!!"
    result = triage_thread(base_thread)
    assert result.suggested_state == WorkItemState.SPAM
    assert result.confidence == ConfidenceBand.LOW

# 5. Date Parsing
def test_triage_date_parsing(base_thread):
    # Timestamp for 2021-01-01 00:00:00 UTC
    base_thread["messages"][0]["internalDate"] = "1609459200000"
    result = triage_thread(base_thread)
    assert result.received_at.year == 2021
    assert result.received_at.month == 1

# 6. Malformed Headers (Missing/Weird Structure)
def test_triage_malformed_headers(base_thread):
    # Headers is None or weird types handling
    # Our code expects list of dicts. If API returns None, .get([], []) handles it?
    # Let's say payload has no headers key
    del base_thread["messages"][0]["payload"]["headers"]
    
    result = triage_thread(base_thread)
    assert result.sender == "unknown"
    assert result.subject == "(No Subject)"
    # Should not crash

# 7. No Body (Metadata Only - Zero Body)
def test_triage_no_body(base_thread):
    # Ensure logic works even if snippet/body is missing
    del base_thread["messages"][0]["snippet"]
    result = triage_thread(base_thread)
    assert result.snippet == ""
    assert result.confidence == ConfidenceBand.MEDIUM # Default

# 8. Large Payload (Stress/Performance)
def test_triage_large_payload(base_thread):
    # Inject massive headers
    large_header = "A" * 10000
    base_thread["messages"][0]["payload"]["headers"].append({"name": "X-Custom", "value": large_header})
    
    # Should process without error
    result = triage_thread(base_thread)
    assert result.thread_id == "t1"

# 9. Encoding/Special Chars
def test_triage_encoding(base_thread):
    base_thread["messages"][0]["payload"]["headers"][0]["value"] = "Sübjéct with Emojis 🚀"
    result = triage_thread(base_thread)
    assert "🚀" in result.subject
    assert "Sübjéct" in result.subject

# 10. Schema Compliance
def test_triage_schema_compliance(base_thread):
    result = triage_thread(base_thread)
    assert isinstance(result, TriageResult)
    # Validate Pydantic
    assert result.model_dump()
