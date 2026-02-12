
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from spine.chapters.admin.safety import SafetyManager
from spine.chapters.action.valve import Valve

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False}, 
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_default_safety_status(session: Session):
    mgr = SafetyManager(session)
    # Default should be operational (kill switch inactive)
    assert mgr.is_kill_switch_active() is False
    status = mgr.get_status()
    assert status["status"] == "OPERATIONAL"

def test_engage_kill_switch(session: Session):
    mgr = SafetyManager(session)
    mgr.engage_kill_switch("admin@test.com")
    
    assert mgr.is_kill_switch_active() is True
    status = mgr.get_status()
    assert status["status"] == "HALTED"
    assert status["updated_by"] == "admin@test.com"

def test_disengage_kill_switch(session: Session):
    mgr = SafetyManager(session)
    mgr.engage_kill_switch("admin@test.com")
    assert mgr.is_kill_switch_active() is True
    
    mgr.disengage_kill_switch("admin@test.com")
    assert mgr.is_kill_switch_active() is False
    assert mgr.get_status()["status"] == "OPERATIONAL"

@pytest.mark.asyncio
async def test_valve_respects_kill_switch(session: Session):
    # Setup Valve with the session engine/factory
    valve = Valve(service_builder=None, session_factory=session.bind)
    
    # 1. Operational - Should Pass Safety Check (fail later at service_builder if wired up, but here we expect it to attempt send)
    # Since we mocked service_builder as None, we expect it to try step 1/2/3.
    # Actually, Valve.send_email will raise Exception at service_builder('gmail'...) if it gets that far.
    # So if it fails with "AttributeError: 'NoneType' object has no attribute '...'" it means it PASSED the safety check.
    
    try:
        await valve.send_email("user", None, "msg", "test@example.com")
    except AttributeError:
         # It passed the safety check and crashed on service_builder (NoneType)
         pass
    except Exception as e:
        # It passed the safety check and crashed on service_builder
        assert "Global Kill Switch is ACTIVE" not in str(e)

    # 2. Engage Kill Switch
    mgr = SafetyManager(session)
    mgr.engage_kill_switch("admin@test.com")
    
    # 3. Halted - Should Fail at Safety Check
    with pytest.raises(RuntimeError) as excinfo:
        await valve.send_email("user", None, "msg", "test@example.com")
    
    assert "Global Kill Switch is ACTIVE" in str(excinfo.value)
