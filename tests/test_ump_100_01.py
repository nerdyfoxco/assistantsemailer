
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from spine.chapters.admin.models import Organization, Tenant, TenantTier, TenantStatus
from spine.chapters.admin.tenants import TenantManager

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

def test_create_org(session: Session):
    mgr = TenantManager(session)
    org = mgr.create_organization("Acme Corp")
    assert org.id is not None
    assert org.name == "Acme Corp"

def test_create_tenant_hierarchy(session: Session):
    mgr = TenantManager(session)
    org = mgr.create_organization("Globex")
    tenant = mgr.create_tenant(org.id, "Globex East", TenantTier.PRO)
    
    assert tenant.organization_id == org.id
    assert tenant.tier == TenantTier.PRO
    assert tenant.status == TenantStatus.ACTIVE

def test_suspend_tenant(session: Session):
    mgr = TenantManager(session)
    org = mgr.create_organization("Umbrella")
    tenant = mgr.create_tenant(org.id, "Raccoon City")
    
    updated = mgr.suspend_tenant(tenant.id)
    assert updated.status == TenantStatus.SUSPENDED

def test_list_tenants(session: Session):
    mgr = TenantManager(session)
    org1 = mgr.create_organization("Org1")
    mgr.create_tenant(org1.id, "T1")
    mgr.create_tenant(org1.id, "T2")
    
    org2 = mgr.create_organization("Org2")
    mgr.create_tenant(org2.id, "T3")
    
    tenants_1 = mgr.list_tenants(org1.id)
    assert len(tenants_1) == 2
    
    tenants_2 = mgr.list_tenants(org2.id)
    assert len(tenants_2) == 1

def test_get_hierarchy(session: Session):
    mgr = TenantManager(session)
    org = mgr.create_organization("MegaCorp")
    mgr.create_tenant(org.id, "Sub1")
    
    data = mgr.get_tenant_hierarchy(org.id)
    assert data["organization"].name == "MegaCorp"
    assert len(data["tenants"]) == 1
    assert data["tenants"][0].name == "Sub1"
